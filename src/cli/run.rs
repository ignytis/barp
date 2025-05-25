use std::collections::{HashMap, VecDeque};
use std::process::{Command as StdCommand, Stdio};

use clap::{ArgAction, Args};
use serde_yaml;

use super::super::types::arg_ref;

#[derive(Args, Clone, Debug)]
pub struct RunArgs {
    #[arg(long = "arg-ref", short = 'a', default_value_t = ("").to_string(),
            help="A reference to arguments which is path to file + arguments ID separated with colon. Example: /my/connfig.cfg:my_args")]
    arg_ref: String,
    #[arg(action = ArgAction::Append, help="Additional arguments to append on top of reference")]
    args: Vec<String>,
}

/// The 'run' command
pub fn run(cmd_args: &RunArgs) {
    let arg_ref_parts: Vec<String> = cmd_args.arg_ref.split(":")
        .map(|x| x.to_string())
        .collect();
    // TODO: check for len of vec
    let path = arg_ref_parts.get(0).unwrap();
    let args_id = arg_ref_parts.get(1).unwrap();

    // TODO: error handling
    let f = std::fs::File::open(path).unwrap();
    // TODO: template rendering goes here
    let d: HashMap<String, arg_ref::TaskArgs> = serde_yaml::from_reader(f).unwrap();

    let args = match d.get(args_id) {
        Some(s) => s,
        None => panic!("Args not found: {}", args_id), // TODO: error handling
    };

    let mut run_args: VecDeque<String> = args.args.as_ref().unwrap().iter()
        .map(|c| c.clone())
        .collect();
    run_args.extend(cmd_args.args.clone());

    let cmd_app = run_args.pop_front().unwrap();
    let output = StdCommand::new(cmd_app)
                        .args(run_args)
                        .stdout(Stdio::piped())
                        .stderr(Stdio::piped())
                        .output()
                        // TODO: error handling
                        .expect("Failure");

    let stdout = String::from_utf8(output.stdout).unwrap();
    println!("{}", stdout);
}
