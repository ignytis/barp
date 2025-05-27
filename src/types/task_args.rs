use std::collections::{HashMap, VecDeque};
use serde::{Serialize, Deserialize};

/// A unit of YAML configuration. Key is always a string,
/// value might be string or collection
#[derive(Debug, Serialize, Deserialize, PartialEq)]
#[serde(untagged)]
pub enum ConfigParam {
    HashMap(HashMap<String, ConfigParam>),
    String(String),
    Vec(Vec<ConfigParam>),
}

/// A list of arguments for task
pub type TaskArgs = VecDeque<String>;