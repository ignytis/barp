use std::collections::{HashMap, VecDeque};
use std::env;

use clap::{ArgAction, Args};

use crate::arg_builders::build_process_params;
use crate::system::run_process;
use crate::types::task_args::{config_param_consume_hashmap_key, config_params_merge, get_task_config_from_reference, ConfigParam};
use crate::yaml::read_yaml_file_as_hashmap;

const ATTR_KIND: &str = "kind";
const ATTR_TASK_DEFAULTS: &str = "task_defaults";

/// Arguments of the 'run' command
#[derive(Args, Clone, Debug)]
pub struct RunArgs {
    #[arg(long = "profile", short = 'p', default_value_t = ("").to_string(),
            help="Path to profile configuration file")]
    profile_path: String,
    #[arg(long = "task-template", short = 't', default_value_t = ("").to_string(),
            help="A reference to task template (path to config file + ID). Example: /my/connfig.cfg:my_args")]
    task_cfg: String,
    #[arg(action = ArgAction::Append, help="Additional arguments to append on top of reference")]
    args: Vec<String>,
}

/// The 'run' command
pub async fn run(run_args: &RunArgs) -> Result<(), String> {
    let mut profile = load_profile(&run_args.profile_path)?;
    // Final task arguments = task defaults from profile (if any) + task arguments in the task template
    let task_cfg_defaults = match config_param_consume_hashmap_key(&mut profile, ATTR_TASK_DEFAULTS)? {
        Some(d) => d,
        None => ConfigParam::HashMap(HashMap::new()),
    };
    let task_cfg = get_task_config_from_reference(&run_args.task_cfg)?;
    let mut task_cfg = config_params_merge(task_cfg_defaults, task_cfg)?;

    // Remove the arg_builder name from configuration because it will not be needed inside
    let arg_builder_name = match config_param_consume_hashmap_key(&mut task_cfg, ATTR_KIND)? {
        Some(x) => match x {
            ConfigParam::String(r) => r,
            _ => return Err(format!("Attribute '{}' is not a string", ATTR_KIND)),
        },
        None => return Err(format!("Key '{}' not found in task configuration", ATTR_KIND)),
    };

    let cmd_args: VecDeque<String> = run_args.args.clone().into();
    let process_params = build_process_params(&arg_builder_name, &task_cfg, &cmd_args)?;
    run_process(&process_params).await
}

fn load_profile(profile_path: &String) -> Result<ConfigParam, String> {
    let profile_path = match profile_path.as_str() {
        "" => env::var("BARP_PROFILE").unwrap_or_default(),
        _ => profile_path.clone(),
    };
    read_yaml_file_as_hashmap(&profile_path)
}
