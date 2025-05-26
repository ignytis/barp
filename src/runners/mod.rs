pub mod command;

use crate::types::task_args::{TaskArgs, TaskConfigRunnerCfg};

/// A runner function
type RunnerFn = fn(cfg: TaskConfigRunnerCfg, args: &TaskArgs);

/// Returns a task funnder by ID
pub fn get_runner(name: &str) -> Option<RunnerFn> {
    match name {
        "command" => Some(command::run_command),
        _ => None,
    }
}