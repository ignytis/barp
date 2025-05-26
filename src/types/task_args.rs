use std::collections::HashMap;
use serde::{Serialize, Deserialize};

/// The main structure of task configuration.
/// Contains common arguments and runner configuration.
#[derive(Serialize, Deserialize, PartialEq, Debug)]
pub struct TaskConfig {
    pub runner: TaskConfigRunner,
    pub args: Option<Vec<String>>,
}

/// Runner arguments: runner name and configuration
#[derive(Serialize, Deserialize, PartialEq, Debug)]
pub struct TaskConfigRunner {
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
