use std::collections::VecDeque;
use std::process::Stdio;

use tokio::io::{AsyncBufReadExt, BufReader};
use tokio::process::Command;
use tokio::signal;

use crate::types::process_params::ProcessParams;

/// Runs a child process using provided parameters
pub async fn run_process(params: &ProcessParams) -> Result<(), String> {
    let mut args: VecDeque<String> = params.args.clone().into();
    let cmd = match args.pop_front() {
        Some(x) => x,
        None => return Err(String::from("Cannot start the process: no command provided")),
    };

    let mut child = Command::new(cmd)
        .args(args)
        .envs(params.env.clone())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .map_err(|e| format!("Failed to spawn a child process: {}", e))?;

    let stdout = BufReader::new(child.stdout.take().unwrap());
    let stderr = BufReader::new(child.stderr.take().unwrap());

    // Spawn output readers
    let stdout_handle = tokio::spawn(async move {
        let mut lines = stdout.lines();
        while let Ok(Some(line)) = lines.next_line().await {
            println!("{}", line);
        }
    });

    let stderr_handle = tokio::spawn(async move {
        let mut lines = stderr.lines();
        while let Ok(Some(line)) = lines.next_line().await {
            eprintln!("{}", line);
        }
    });

    // Wait for either Ctrl+C or process exit
    tokio::select! {
        _ = signal::ctrl_c() => {
            println!("\nReceived Ctrl+C, killing child process...");
            let _ = child.kill().await;
        }
        status = child.wait() => {
            match status {
                Ok(status) => {
                    let code = match status.code() {
                        Some(c) => format!("{}", c),
                        None => format!("(not exit code)"),
                    };
                    println!("Process exited with code {}", code);
                },
                Err(e) => return Err(format!("Execution failed: {}", e)),
            }
        }
    }

    // Ensure all output is printed
    let _ = stdout_handle.await;
    let _ = stderr_handle.await;

    Ok(())
}