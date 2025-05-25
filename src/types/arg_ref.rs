use std::collections::HashMap;
use serde::{Serialize, Deserialize};

/// The main structure of arg reference.
/// Contains common arguments and runner configuration.
#[derive(Serialize, Deserialize, PartialEq, Debug)]
pub struct TaskArgs {
    pub runner: TaskArgsRunner,
    pub args: Option<Vec<String>>,
}

/// Runner arguments: runner name and configuration
#[derive(Serialize, Deserialize, PartialEq, Debug)]
pub struct TaskArgsRunner {
    pub name: String,
    pub config: Option<HashMap<String, ConfigParam>>,
}

/// A unit of YAML configuration. Key is always a string,
/// value might be string or nested structure
#[derive(Debug, Serialize, Deserialize, PartialEq)]
#[serde(untagged)]
pub enum ConfigParam {
    String(String),
    HashMap(HashMap<String, ConfigParam>)
}
