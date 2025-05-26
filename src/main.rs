mod cli;
mod runners;
mod types;

fn main() -> Result<(), String> {
    cli::router()
}

