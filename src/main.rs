mod arg_builders;
mod cli;
mod system;
mod types;
mod yaml;

fn main() -> Result<(), String> {
    cli::router()
}

