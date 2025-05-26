use std::collections::{HashMap, VecDeque};

use clap::{ArgAction, Args};
use serde_yaml;

use crate::runners;
use crate::types::task_args::TaskConfig;

#[derive(Args, Clone, Debug)]
pub struct RunArgs {
    #[arg(long = "cfg-ref", short = 'c', default_value_t = ("").to_string(),
            help="A reference to task configuration (path + ID). Example: /my/connfig.cfg:my_args")]
    task_cfg_ref: String,
    #[arg(action = ArgAction::Append, help="Additional arguments to append on top of reference")]
    args: Vec<String>,
}

/// The 'run' command
pub fn run(cmd_args: &RunArgs) -> Result<(), String> {
    let task_cfg = get_task_config_from_reference(&cmd_args.task_cfg_ref)?;

    let runner_fn = match runners::get_runner(&task_cfg.runner.name) {
        Some(r) => r,
        None => return Err(format!("Cannot find a runder by name: {}", &task_cfg.runner.name)),
    };

    let mut run_args: VecDeque<String> = task_cfg.args.as_ref().unwrap().iter()
        .map(|c| c.clone())
        .collect();
    run_args.extend(cmd_args.args.clone());

    runner_fn(task_cfg.runner.config, &run_args);
    Ok(())
}

/// Returns an instance of Task Arguments from reference
/// Format of referecence is 'path:id' where path is path to configuration file and ID is task configuration ID
fn get_task_config_from_reference(task_cfg_ref: &String) -> Result<TaskConfig, String> {
    let arg_ref_parts: Vec<String> = task_cfg_ref.split(":")
        .map(|x| x.to_string())
        .collect();
    if arg_ref_parts.len() != 2 {
        return Err(format!("Invalid format of argument reference '{}'. It should be path to file and reference ID separated with colon. Example: /tmp/myfile.cfg:my_task", task_cfg_ref))
    }
    let path = arg_ref_parts.get(0).unwrap();
    let args_id = arg_ref_parts.get(1).unwrap();

    let file = match std::fs::File::open(path) {
        Ok(f) => f,
        Err(e) => return Err(format!("Failed to open a file: {}", e))
    };
    // TODO: template rendering goes here
    let mut file_contents: HashMap<String, TaskConfig> = serde_yaml::from_reader(file).unwrap();
    match file_contents.remove(args_id) {
        Some(s) => Ok(s),
        None => Err(format!("Task configuration with ID '{}' not found in file '{}'", args_id, path))
    }
}