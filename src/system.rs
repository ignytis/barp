use std::process::{Command, Stdio};

use crate::types::process_params::ProcessParams;

pub fn run_process(params: &ProcessParams) {
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