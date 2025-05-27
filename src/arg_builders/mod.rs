pub mod command;

use crate::types::{
    process_params::ProcessParams,
    task_args::{ConfigParam, TaskArgs}
};


/// Argument builder is a function which builds the process execution parameters
type ArgBuilderFn = fn(cfg: &ConfigParam, args: &TaskArgs) -> Result<ProcessParams, String>;

/// Returns a task funnder by ID
pub fn get_arg_builder(name: &str) -> Option<ArgBuilderFn> {
    match name {
        "command" => Some(command::run_command),
        _ => None,
    }
}