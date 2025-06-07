pub mod run;

use clap::{Parser, Subcommand};

/// A tool for execution of pre-configured commands.
#[derive(Debug, Parser)]
#[clap(name = "barp", version)]
pub struct App {
    #[clap(subcommand)]
    cmd: Command,
}

/// Possible commands are listed here
#[derive(Debug, Subcommand, Clone)]
enum Command {
    /// Runs a command
    Run(run::RunArgs)
}

/// This function is called from main() and does the rest of work
pub async fn router() -> Result<(), String> {
    let app = App::parse();
    match &app.cmd {
        Command::Run(r) => run::run(r).await,
    }
}