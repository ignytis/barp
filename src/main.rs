mod arg_builders;
mod cli;
mod system;
mod types;
mod yaml;

#[tokio::main]
async fn main() -> Result<(), String> {
    cli::router().await
}

