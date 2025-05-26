use crate::types::task_args::{TaskArgs, TaskConfigRunnerCfg};

use std::process::{Command, Stdio};

/// Runs a tasks as a system command
/// TODO: use config to pass environment variables and maybe other config
pub fn run_command(_cfg: TaskConfigRunnerCfg, args: &TaskArgs) {
    let mut args = args.clone();
    let cmd_app = args.pop_front().unwrap();
    let output = Command::new(cmd_app)
                        .args(args)
                        .stdout(Stdio::piped())
                        .stderr(Stdio::piped())
                        .output()
                        // TODO: error handling
                        .expect("Failure");

    let stdout = String::from_utf8(output.stdout).unwrap();
    println!("{}", stdout);
}