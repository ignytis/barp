use std::collections::HashMap;

use crate::types::task_args::{config_param_get_key_as_string_kv_hashmap, ConfigParam};

#[derive(Debug, Default)]
/// Parameters of process to run
pub struct ProcessParams {
    /// Command line arguments for command
    pub args: Vec<String>,
    /// Environment variables
    pub env: HashMap<String, String>,
}

impl TryFrom<&ConfigParam> for ProcessParams {
    type Error = String;

    fn try_from(value: &ConfigParam) -> Result<ProcessParams, String> {
        let mut result = ProcessParams::default();

        let value_map = match value {
            ConfigParam::HashMap(m) => m,
            _ => return Err(String::from("Cannot initialize the process parameters: the provided config is not a hashmap")),
        };
        // Resolve arguments
        let value_args = match value_map.get("args") {
            Some(x) => match x {
                ConfigParam::Vec(v) => v.clone(),
                _ => return Err(String::from("Cannot initialize the process parameters: the 'args' property is not a vector")),
            },
            None => Vec::new(),
        };
        result.args = value_args.iter()
            .filter_map(|x| match x {
                ConfigParam::String(s) => Some(s.clone()),
                _ => None,
            })
            .collect();
        result.env = match config_param_get_key_as_string_kv_hashmap(&value, "env") {
            Ok(o) => match o {
                Some(r) => r,
                None => HashMap::new(),
            },
            Err(e) => return Err(format!("Failed to read the environment variable configuration: {}", e))
        };

        Ok(result)
    }
}
