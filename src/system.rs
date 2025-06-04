use std::{collections::VecDeque, process::{Command, Stdio}};

use crate::types::process_params::ProcessParams;

pub fn run_process(params: &ProcessParams) -> Result<(), String> {
    let mut args: VecDeque<String> = params.args.clone().into();
    let cmd = match args.pop_front() {
        Some(x) => x,
        None => return Err(String::from("Cannot start the process: no command provided")),
    };

    let result = Command::new(cmd)
        .args(args.clone())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .output();

    let output = match result {
        Ok(r) => r,
        Err(e) => return Err(format!("Execution failed: {}", e))
    };

    let stdout = String::from_utf8(output.stdout).unwrap();
    println!("{}", stdout);
    Ok(())
}