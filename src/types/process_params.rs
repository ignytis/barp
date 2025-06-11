use std::collections::HashMap;

use mlua::FromLua;

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

impl FromLua for ProcessParams {
    fn from_lua(value: mlua::Value, _lua: &mlua::Lua) -> mlua::Result<Self> {
        let mut result = ProcessParams::default();
        let lua_table = match value {
            mlua::Value::Table(t) => t,
            _ => return mlua::Result::Err(mlua::Error::FromLuaConversionError { from: "table", to: format!("ProcessParams"),
                message: Some(format!("Expected a table from run() Lua function, but got another type")) }),
        };
        result.args = match lua_table.get("args") {
            Ok(r) => r,
            Err(e) => return mlua::Result::Err(mlua::Error::FromLuaConversionError { from: "table", to: format!("ProcessParams"),
                message: Some(format!("Failed to read 'args' from run() Lua function response: {}", e)) }),
        };
        result.env = match lua_table.get("env") {
            Ok(r) => r,
            Err(e) => return mlua::Result::Err(mlua::Error::FromLuaConversionError { from: "table", to: format!("ProcessParams"),
                message: Some(format!("Failed to read 'env' from run() Lua function response: {}", e)) }),
        };

        mlua::Result::Ok(result)
    }
}