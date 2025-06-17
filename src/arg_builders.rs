use std::collections::{HashMap, VecDeque};

use mlua::Lua;
use walkdir::WalkDir;

use crate::system::get_arg_builders_dir;
use crate::types::process_params::ProcessParams;
use crate::types::task_args::{config_param_get_hashmap_key, config_param_get_key_as_string_kv_hashmap, ConfigParam};
use crate::types::task_config::ATTR_TASK_DEFAULTS;


#[derive(Clone)]
pub struct BuildProcessParamsArgs {
    pub cmd_args: VecDeque<String>,
    pub builder_name: String,
    pub profile: ConfigParam,
    pub task_cfg: ConfigParam,
}

/// Builds parameters for process execution
pub fn build_process_params(args: &BuildProcessParamsArgs) -> Result<ProcessParams, String> {
    let params = match args.builder_name.as_str() {
        "command" => build_params_for_command(args),
        _ => build_params_with_lua(args),
    }?;
    Ok(params)
}

/// A standard builder function for tasks of 'command' type
fn build_params_for_command(args: &BuildProcessParamsArgs) -> Result<ProcessParams, String> {
    let mut process_params: ProcessParams = (&args.task_cfg).try_into()?;
    // Append the command line arguments to argument defaults from task config
    process_params.args.extend(args.cmd_args.clone());

    let task_defaults = match config_param_get_hashmap_key(&args.profile, ATTR_TASK_DEFAULTS) {
        Ok(o) => match o {
            Some(c) => c,
            None => ConfigParam::HashMap(HashMap::new()),
        },
        Err(e) => return Err(format!("Failed to read the task default config from profile: {}", e))
    };

    let mut env = match config_param_get_key_as_string_kv_hashmap(&task_defaults, "env") {
        Ok(o) => match o {
            Some(v) => v,
            None => HashMap::new(),
        },
        Err(e) => return Err(format!("Failed to read the env config from profile: {}", e))
    };
    let env_task = match config_param_get_key_as_string_kv_hashmap(&args.task_cfg, "env") {
        Ok(o) => match o {
            Some(c) => c,
            None => HashMap::new(),
        },
        Err(e) => return Err(format!("Failed to read the env config from profile: {}", e))
    };
    env.extend(env_task);
    process_params.env = env;

    Ok(process_params)
}

/// Looks up the argument builder across Lua scripts
fn build_params_with_lua(args: &BuildProcessParamsArgs) -> Result<ProcessParams, String> {
    // Re-use the logic for command line. Lua will be added on top of it.
    let process_params: ProcessParams = build_params_for_command(&args)?;
    
    let lua = match lua_get_env_for_arg_builder(&args.builder_name)? {
        Some(l) => l,
        None => return Err(format!("Arg builder '{}' not found", args.builder_name))
    };
    
    let run_func = lua.globals().get::<mlua::Function>("build").unwrap();
    let args_final: ProcessParams = match run_func.call((process_params.args, process_params.env.clone())) {
        Ok(r) => r,
        Err(e) => return Err(format!("Lua function call failed: {}", e)),
    };

    Ok(args_final)
}

/// Returns a Lua environment with loaded functions for builder with provided name
fn lua_get_env_for_arg_builder(builder_name: &String) -> Result<Option<Lua>, String> {
    let lua = Lua::new();
    // Locate a Lua script file which arg parser ID matches to the one provided in arguments
    let arg_builders_dir = match get_arg_builders_dir() {
        Ok(d) => d,
        Err(e) => return Err(format!("Failed to locate the argument builders directory: {}", e)),
    };
    let lua_files: Vec<String> = WalkDir::new(arg_builders_dir)
        .into_iter()
        .filter_map(Result::ok)
        .filter(|entry| {
            entry.file_type().is_file() &&
            entry.path().extension().map_or(false, |ext| ext == "lua")
        })
        .map(|entry| entry.path().to_string_lossy().into_owned())
        .collect();

    for lua_file_path in lua_files {
        let file = match std::fs::read_to_string(&lua_file_path) {
            Ok(f) => f,
            Err(e) => return Err(format!("Failed to open a Lua script '{}': {}", lua_file_path, e))
        };

        lua.load(file).exec().unwrap();

        let id_func = lua.globals().get::<mlua::Function>("id").unwrap();
        let lua_builder_name: String = id_func.call(()).unwrap();
        if &lua_builder_name == builder_name {
            return Ok(Some(lua))
        }
    }

    return Ok(None)
}