use std::collections::{HashMap, VecDeque};
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
    pub config: TaskConfigRunnerCfg,
}

/// A unit of YAML configuration. Key is always a string,
/// value might be string or nested structure
#[derive(Debug, Serialize, Deserialize, PartialEq)]
#[serde(untagged)]
pub enum ConfigParam {
    String(String),
    HashMap(HashMap<String, ConfigParam>)
}

/// Runner-specific configuration in 'runner.config' section
pub type TaskConfigRunnerCfg = Option<HashMap<String, ConfigParam>>;

/// A list of arguments for task
pub type TaskArgs = VecDeque<String>;