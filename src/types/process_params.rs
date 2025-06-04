use std::collections::VecDeque;

use serde::{Deserialize, Serialize};

#[derive(Default)]
/// Parameters of process to run
pub struct ProcessParams {
    /// Command line arguments for command
    pub args: Vec<String>,
    /// Command to execute. Typically it's an application name
    pub command: String,
}

/// TODO: replace with ProcessParams? These are doing the same job
#[derive(Serialize, Deserialize, PartialEq, Debug)]
pub struct CommandArgs {
    pub args: VecDeque<String>,
}
