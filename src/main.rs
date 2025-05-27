mod arg_builders;
mod cli;
mod serialization;
mod system;
mod types;

fn main() -> Result<(), String> {
    cli::router()
}

