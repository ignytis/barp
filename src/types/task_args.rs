use std::collections::HashMap;

use crate::yaml::read_yaml_file_as_hashmap;

/// A unit of YAML configuration. Key is always a string,
/// value might be string or collection
#[derive(Debug, PartialEq, Clone)]
pub enum ConfigParam {
    Boolean(bool),
    HashMap(HashMap<String, ConfigParam>),
    Int(i64),
    Null,
    String(String),
    Vec(Vec<ConfigParam>),
}

/// Returns a parameter by key.
/// Unlike config_param_consume_hashmap_key, doesn't remove the key from collection
pub fn config_param_get_hashmap_key<S: Into<String>>(cfg: &ConfigParam, key: S)
        -> Result<Option<ConfigParam>, String> {
    match cfg {
        ConfigParam::HashMap(m) => {
            match m.get(&key.into()) {
                Some(x) => Ok(Some(x.clone())),
                None => Ok(None),
            }
            
        },
        _ => return Err(format!("The provided config is not a hashmap: {:?}", cfg)),
    }
}

/// Merges two configuration params into new instance of configuration params
/// Collections are merged for sure. In case of scalar values - return the second value
pub fn config_params_merge(first: ConfigParam, second: ConfigParam) -> Result<ConfigParam, String> {
    match first {
        ConfigParam::HashMap(m_first) => {
            match second {
                ConfigParam::HashMap(m_second) => {
                    let mut result: HashMap<String, ConfigParam> = HashMap::new();
                    for (k, v) in &m_first {
                        result.insert(k.clone(), v.clone());
                    }
                    for (k, v) in &m_second {
                        result.insert(k.clone(), v.clone());
                    }
                    Ok(ConfigParam::HashMap(result))
                },
                _ => return Err(String::from("The first item is hashmap, the second is not")),
            }
        },
        ConfigParam::Vec(v_first) => {
            match second {
                ConfigParam::Vec(v_second) => {
                    Ok(ConfigParam::Vec(v_first.iter().chain(v_second.iter()).cloned().collect()))
                },
                _ => return Err(String::from("The first item is vector, the second is not")),
            }
        },
        _ => Ok(second.clone()),
    }
}

/// Returns a property of provided config as a haspmap where keys and values are strings.
/// Returns an error if provided collection or requested key are not hashmaps.
pub fn config_param_get_key_as_string_kv_hashmap<S: Into<String>>(config_param: &ConfigParam, key: S) -> Result<Option<HashMap<String, String>>, String> {
    let key: String = key.into();
    let config_param_map = match config_param {
        ConfigParam::HashMap(m) => m,
        _ => return Err(format!("Cannot read a key '{}' into hashmap: the type of provided config is not hashmap", key)),
    };

    let config_param_map = match config_param_map.get(&key) {
        Some(x) => match x {
            ConfigParam::HashMap(v) => v.clone(),
            _ => return Err(format!("Cannot read a key '{}' into hashmap: this attribute is not hashmap", &key)),
        },
        None => return Ok(None),
    };
    let v: HashMap<String, String> = config_param_map.iter()
        .map(|(k, v)| {
            let v2 = match v {
                ConfigParam::String(v) => v.clone(),
                ConfigParam::Int(v) => format!("{}", v),
                _ => return Err(format!("Invalid data type of environment variable '{}'. It must be string or integer", k.clone()))
            };
            Ok((k.clone(), v2))
        })
        .collect::<Result<_, _>>()?;
    Ok(Some(v))
}

/// Returns an instance of task config from reference
/// Format of referecence is 'path:id' where path is path to configuration file and ID is task configuration ID
pub fn get_task_config_from_reference(task_cfg_ref: &String) -> Result<ConfigParam, String> {
    let arg_ref_parts: Vec<String> = task_cfg_ref.split(":")
        .map(|x| x.to_string())
        .collect();
    if arg_ref_parts.len() != 2 {
        return Err(format!("Invalid format of argument reference '{}'. It should be path to file and reference ID separated with colon. Example: /tmp/myfile.cfg:my_task", task_cfg_ref))
    }
    let path = arg_ref_parts.get(0).unwrap();
    let args_id = arg_ref_parts.get(1).unwrap();

    let file_contents = read_yaml_file_as_hashmap(&path)?;
    let task_cfg = match file_contents {
        ConfigParam::HashMap(m) => m.clone(),
        _ => return Err(String::from("The task configuration is not a hashmap")),
    };
    match task_cfg.get(args_id) {
        Some(c) => Ok(c.clone()),
        None => return Err(format!("Task configuration with ID '{}' not found in file '{}'", args_id, path))
    }
}