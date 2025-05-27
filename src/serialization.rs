use serde::{de::DeserializeOwned, Serialize};

/// Maps object of type X into object of type Y using serialization
pub fn map_objects<X, Y>(from: &X) -> Result<Y, String>
where 
    X: Serialize,
    Y: DeserializeOwned
{
    let serialized = match serde_yaml::to_string(from) {
        Ok(c) => c,
        Err(e) => return Err(format!("Failed to serialize an object: {}", e)),
    };
    match serde_yaml::from_str(&serialized) {
        Ok(c) => Ok(c),
        Err(e) => return Err(format!("Failed to deserialize an object: {}", e)),
    }
}