use std::collections::VecDeque;

use mlua::Lua;

use crate::types::process_params::ProcessParams;
use crate::types::task_args::ConfigParam;


/// Builds parameters for process execution
pub fn build_process_params(arg_builder_name: &String, task_cfg: &ConfigParam, cmd_args: &VecDeque<String>) -> Result<ProcessParams, String> {
    let params = match arg_builder_name.as_str() {
        "command" => build_params_for_command(task_cfg, cmd_args),
        _ => build_params_with_lua(arg_builder_name, task_cfg, cmd_args),
    }?;
    Ok(params)
}

/// A standard builder function for tasks of 'command' type
fn build_params_for_command(task_cfg: &ConfigParam, cmd_args: &VecDeque<String>) -> Result<ProcessParams, String> {
    let process_params: ProcessParams = task_cfg.try_into()?;
    let mut args_final = process_params.args.clone();
    args_final.extend(cmd_args.clone());
    Ok((&args_final).into())
}

/// Looks up the argument builder across Lua scripts
fn build_params_with_lua(arg_builder_name: &String, task_cfg: &ConfigParam, cmd_args: &VecDeque<String>) -> Result<ProcessParams, String> {
    let process_params: ProcessParams = task_cfg.try_into()?;
    let mut args_final = process_params.args.clone();
    args_final.extend(cmd_args.clone());

    
    let path = "docs/examples/barp.d/arg_builders/docker.lua";
    let file = match std::fs::read_to_string(path) {
        Ok(f) => f,
        Err(e) => return Err(format!("Failed to open a Lua script '{}': {}", path, e))
    };

    let lua = Lua::new();
    lua.load(file).exec().unwrap();

    let id_func = lua.globals().get::<mlua::Function>("id").unwrap();
    let builder_name: String = id_func.call(()).unwrap();
    if &builder_name != arg_builder_name {
        return Err(format!("Arg builder '{}' not found", arg_builder_name))
    }
    
    
    let run_func = lua.globals().get::<mlua::Function>("build").unwrap();
    let args_final: Vec<String> = match run_func.call(args_final) {
        Ok(r) => r,
        Err(e) => return Err(format!("Lua function call failed: {}", e)),
    };

    Ok((&args_final).into())
}