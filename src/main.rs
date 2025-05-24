use std::collections::HashMap;

use clap::{ArgAction, Parser, Subcommand};

use serde::{Serialize, Deserialize};
use serde_yaml;

#[derive(Debug, Parser)]
#[clap(name = "barp", version)]
pub struct App {
    #[clap(subcommand)]
    cmd: Command,
}

#[derive(Debug, Subcommand, Clone)]
enum Command {
    Run {
        #[arg(long = "arg-ref", short = 'a', default_value_t = ("").to_string(),
              help="A reference to arguments which is path to file + arguments ID separated with colon. Example: /my/connfig.cfg:my_args")]
        arg_ref: String,
        #[arg(action = ArgAction::Append, help="Additional arguments to append on top of reference")]
        args: Vec<String>,
    },
}


#[derive(Serialize, Deserialize, PartialEq, Debug)]
struct TaskArgsRunner {
    name: String,
    config: Option<HashMap<String, String>>,
}

#[derive(Serialize, Deserialize, PartialEq, Debug)]
struct TaskArgs {
    runner: TaskArgsRunner,
    env: Option<HashMap<String, String>>,
    args: Option<Vec<String>>,
}

fn main() {
    let app = App::parse();
    match &app.cmd {
        Command::Run { arg_ref, args } => run(arg_ref, args),
    }
}

fn run(arg_ref: &String, additional_args: &Vec<String>) {
    let arg_ref_parts: Vec<String> = arg_ref.split(":")
        .map(|x| x.to_string())
        .collect();
    // TODO: check for len of vec
    let path = arg_ref_parts.get(0).unwrap();
    let args_id = arg_ref_parts.get(1).unwrap();

    // TODO: error handling
    let f = std::fs::File::open(path).unwrap();
    // TODO: template rendering goes here
    let d: HashMap<String, TaskArgs> = serde_yaml::from_reader(f).unwrap();

    let args = match d.get(args_id) {
        Some(s) => s,
        None => panic!("Args not found: {}", args_id), // TODO: error handling
    };

    let mut args: Vec<String> = args.args.as_ref().unwrap().clone();
    args.extend(additional_args.clone());
    for arg in args {
        println!("AAA: {}", arg);
    }
}
