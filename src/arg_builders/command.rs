use crate::types::{
    process_params::ProcessParams,
    task_args::{ConfigParam, TaskArgs}
};

use std::collections::VecDeque;

use serde::{Deserialize, Serialize};
use serde_yaml;

#[derive(Serialize, Deserialize, PartialEq, Debug)]
struct CommandArgs {
    env: ConfigParam,
    args: VecDeque<String>,
}

/// Runs a tasks as a system command
pub fn run_command(cfg: &ConfigParam, args: &TaskArgs) -> Result<ProcessParams, String> {
    let cfg = serde_yaml::to_string(cfg).unwrap();
    let cfg: CommandArgs = serde_yaml::from_str(&cfg).unwrap();

    let mut args_final = cfg.args.clone();
    let mut args = args.clone();
    args_final.append(&mut args);

    let mut params = ProcessParams::default();
    params.command = match args_final.pop_front() {
        Some(p) => p,
        None => return Err(String::from("Command is not specified")),
    };
    params.args = args_final.into();

    Ok(params)
}