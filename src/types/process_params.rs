use std::collections::HashMap;

use crate::types::task_args::ConfigParam;

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
        // Resolve the env vars
        let env = match value_map.get("env") {
            Some(x) => match x {
                ConfigParam::HashMap(v) => v.clone(),
                _ => return Err(String::from("Cannot initialize the process parameters: the 'env' property is not a hashmap")),
            },
            None => HashMap::new(),
        };
        let env: HashMap<String, String> = env.iter()
            .map(|(k, v)| {
                let v2 = match v {
                    ConfigParam::String(v) => v.clone(),
                    ConfigParam::Int(v) => format!("{}", v),
                    _ => return Err(format!("Invalid data type of environment variable '{}'. It must be string or integer", k.clone()))
                };
                Ok((k.clone(), v2))
            })
            .collect::<Result<_, _>>()?;
        result.env = env;

        Ok(result)
    }
}
