use std::collections::{HashMap, VecDeque};
use std::process::{Command, Stdio};

use clap::{ArgAction, Args};
use serde_yaml;

use crate::arg_builders;
use crate::types::process_params::ProcessParams;
use crate::types::task_args::ConfigParam;

const ATTR_KIND: &str = "kind";

#[derive(Args, Clone, Debug)]
pub struct RunArgs {
    #[arg(long = "cfg-ref", short = 'c', default_value_t = ("").to_string(),
            help="A reference to task configuration (path + ID). Example: /my/connfig.cfg:my_args")]
    task_cfg_ref: String,
    #[arg(action = ArgAction::Append, help="Additional arguments to append on top of reference")]
    args: Vec<String>,
}

/// The 'run' command
pub fn run(run_args: &RunArgs) -> Result<(), String> {
    let mut task_cfg = get_task_config_from_reference(&run_args.task_cfg_ref)?;

    // Remove the arg_builder name from configuration because it will not be needed inside
    let arg_builder_name = match task_cfg.remove(ATTR_KIND) {
        Some(ConfigParam::String(r)) => r,
        Some(_) => return Err(format!("Attribute '{}' is not a string", ATTR_KIND)),
        None => return Err(format!("Attribute '{}' is missing in task configuration", ATTR_KIND)),
    };
    let arg_builder_fn = match arg_builders::get_arg_builder(&arg_builder_name) {
        Some(r) => r,
        None => return Err(format!("Cannot find a runder by name: {}", &arg_builder_name)),
    };

    // Downcast the task config from hashmap into parameter structure
    let task_cfg = match serde_yaml::to_string(&task_cfg) {
        Ok(c) => c,
        Err(e) => return Err(format!("Failed to serialize the task config: {}", e)),
    };
    let task_cfg: ConfigParam = match serde_yaml::from_str(&task_cfg) {
        Ok(c) => c,
        Err(e) => return Err(format!("Failed to deserialize the task config: {}", e)),
    };

    let cmd_args: VecDeque<String> = run_args.args.clone().into();

    let process_params = match arg_builder_fn(&task_cfg, &cmd_args) {
        Ok(p) => p,
        Err(e) => return Err(format!("Failed to deserialize the task config: {}", e)),
    };
    do_run(&process_params);
    Ok(())
}

/// Returns an instance of Task Arguments from reference
/// Format of referecence is 'path:id' where path is path to configuration file and ID is task configuration ID
fn get_task_config_from_reference(task_cfg_ref: &String) -> Result<HashMap<String, ConfigParam>, String> {
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
    let mut file_contents: HashMap<String, HashMap<String, ConfigParam>> = serde_yaml::from_reader(file).unwrap();
    match file_contents.remove(args_id) {
        Some(s) => Ok(s),
        None => Err(format!("Task configuration with ID '{}' not found in file '{}'", args_id, path))
    }
}

fn do_run(params: &ProcessParams) {
    let output = Command::new(params.command.clone())
        .args(params.args.clone())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .output()
        // TODO: error handling
        .expect("Failure");

    let stdout = String::from_utf8(output.stdout).unwrap();
    println!("{}", stdout);
}