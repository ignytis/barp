# Barp: Build Arguments, Run Process

## Trivia

This application simplifies execution of processes by providing a flexible way to define arguments.

## Status

Early WIP

## Examples of execution

__Basic execution via command line arguments:__

```bash
$ barp run \
    -p $PWD/docs/examples/barp.d/profiles/local.cfg \
    -t $PWD/docs/examples/barp.d/task_templates/command.cfg:print_n_times

Hello 1 🚀
Hello 2 🚀
Hello 3 🚀
Hello 4 🚀
Hello 5 🚀
Example error! 💥
```

__Using profile + CLI arguments only:__

If the task template parameter is skipped, the empty template will be used.
It might be useful for system commands:

```bash
$ barp run -p $PWD/docs/examples/barp.d/profiles/local.cfg -- printenv | grep BARP

BARP_SAMPLE_PROFILE_VAR_A=profile_env_val_env
BARP_SAMPLE_PROFILE_VAR_C=
BARP_SAMPLE_PROFILE_VAR_D=profile_env_val_task
```
Since `command` is a default task type in profile `docs/examples/barp.d/profiles/local.cfg`,
the provided arguments automatically resolve into system command.
The environment variables also come from profile confiuguration.

__Composing profile from multiple configuration files:__

_Case 1. Using 'local' profile only:_

```bash
barp run \
    -p $PWD/docs/examples/barp.d/profiles/local.cfg \
    -t $PWD/docs/examples/barp.d/task_templates/command.cfg:print_env_vars

BARP_SAMPLE_PROFILE_VAR_A=profile_env_val_env
BARP_SAMPLE_PROFILE_VAR_C=
BARP_SAMPLE_PROFILE_VAR_D=profile_env_val_task
BARP_SAMPLE_TASK_VAR_A=task_test
```

_Case 2. Using 'common' profile is added:_

```bash
barp run \
    -p $PWD/docs/examples/barp.d/profiles/common.cfg:$PWD/docs/examples/barp.d/profiles/local.cfg \
    -t $PWD/docs/examples/barp.d/task_templates/command.cfg:print_env_vars

BARP_SAMPLE_PROFILE_VAR_A=profile_env_val_env
BARP_SAMPLE_PROFILE_VAR_B=profile_env_val_b
BARP_SAMPLE_PROFILE_VAR_C=append_profile_env_val_b
BARP_SAMPLE_PROFILE_VAR_D=profile_env_val_task
BARP_SAMPLE_TASK_VAR_A=task_test
```

__Adjusting the environment via env vars:__

```bash
# Local process
$ export BARP_PROFILE=$PWD/docs/examples/barp.d/profiles/local.cfg
$ barp run -t $PWD/docs/examples/barp.d/task_templates/command.cfg:print_env_vars
Here is an env var from task: "test"; Here is an env var from profile: "abc"

# Docker. NB: Docker needs to be running
$ export BARP_PROFILE=$PWD/docs/examples/barp.d/profiles/docker.cfg
$ barp run -t $PWD/docs/examples/barp.d/task_templates/command.cfg:print_env_vars
Here is an env var from task: "test"; Here is an env var from profile: "abc_docker"
```

## Some ideas for implementation

### Event listeners

Catch events like "before task start", "after task end", etc

### Task transformers

If task template is incompatible with some executor, transformers could convert it into compatible one.

### Project management

Combine tasks into projects + compile projects, like Apache Airflow

## Standard library of executors

- Kubernetes job
- SSH
- Python file