use std::collections::HashMap;

use yaml_rust::{Yaml, YamlLoader};

use crate::types::task_args::ConfigParam;

/// Returns a YAML document as an instance of ConfigParam struct
pub fn read_yaml_file_as_hashmap(path: &String) -> Result<ConfigParam, String> {
    let contents = match std::fs::read_to_string(path) {
        Ok(c) => c,
        Err(e) => return Err(format!("Failed to read the YAML file '{path}': {}", e)),
    };

    let yaml_doc = match YamlLoader::load_from_str(&contents) {
        Ok(s) => s,
        Err(e) => return Err(format!("Failed to parse the contents of YAML profile: {}", e)),
    };

    // YAML lib returns the result as vector; take the first element only
    let y = match yaml_doc.get(0) {
        None => return Err(String::from("Profile config must be a map, but a list is provided instead.")),
        Some(p) => p.clone(),
    };
    match y {
        Yaml::Hash(_) => yaml_to_config(&y),
        _ => Err(String::from("Unexpected YAML content. The expected type is hashmap")),
    }
}

/// Converts the YAML document into ConfigParam.
/// We are using ConfigParam instead of YAML document in the code
/// in order to encapsulate the YAML library internals.
fn yaml_to_config(yml: &Yaml) -> Result<ConfigParam, String> {
    let result = match yml {
        Yaml::Alias(_) => return Err(format!("Unsupported type: alias in YAML")),
        Yaml::Array(v) => {
            let mut result_vec: Vec<ConfigParam> = Vec::with_capacity(v.len());
            for i in v {
                result_vec.push(yaml_to_config(i)?);
            }
            ConfigParam::Vec(result_vec)
        },
        Yaml::BadValue => return Err(format!("Bad value in YAML")),
        Yaml::Boolean(v) => ConfigParam::Boolean(*v),
        Yaml::Hash(kv) => {
            let mut result_map: HashMap<String, ConfigParam> = HashMap::new();
            for (k, v) in kv.iter() {
                // TODO: add checks in case if key is a NOT string
                let k = k.clone().into_string().unwrap();
                let v = yaml_to_config(v)?;
                result_map.insert(k, v);
            }
            ConfigParam::HashMap(result_map)
        }
        Yaml::Integer(v) => ConfigParam::Int(*v),
        Yaml::Null => ConfigParam::Null,
        // TODO: should we keep string here, the same as Yaml does,
        // or float is needed?
        Yaml::Real(v) => ConfigParam::String(v.clone()),
        Yaml::String(v) => ConfigParam::String(v.clone()),
    };
    Ok(result)
}