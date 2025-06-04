use crate::types::task_args::ConfigParam;

#[derive(Default)]
/// Parameters of process to run
pub struct ProcessParams {
    /// Command line arguments for command
    pub args: Vec<String>,
}

impl TryFrom<&ConfigParam> for ProcessParams {
    type Error = String;

    fn try_from(value: &ConfigParam) -> Result<ProcessParams, String> {
        let value_map = match value {
            ConfigParam::HashMap(m) => m,
            _ => return Err(String::from("Cannot initialize the process parameters: the provided config is not a hashmap")),
        };
        let mut result = ProcessParams::default();
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

        Ok(result)
    }
}

impl From<&Vec<String>> for ProcessParams {
    fn from(value: &Vec<String>) -> Self {
        let mut result = ProcessParams::default();
        result.args = value.clone();
        result
    }
}