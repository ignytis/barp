#[derive(Default)]
/// Parameters of process to run
pub struct ProcessParams {
    /// Command to execute. Typically it's an application name
    pub command: String,
    /// Command line arguments for command
    pub args: Vec<String>,
}