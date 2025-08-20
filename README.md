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
    file://$PWD/docs/examples/barp.d/task_templates/command.cfg?command.print_n_times

Hello 1 🚀
Hello 2 🚀
Hello 3 🚀
Hello 4 🚀
Hello 5 🚀
Example error! 💥
```

__Execution from standard input__

```bash
$ barp run \
    -p $PWD/docs/examples/barp.d/profiles/local.cfg \
    - \
    one two three < $PWD/docs/examples/barp.d/task_templates/stdin.cfg

Hello, World! There are more arguments will be printed if any provided:  one two three
```
or:
```bash
$ barp run \
    -p $PWD/docs/examples/barp.d/profiles/local.cfg \
    stdin:// \
    one two three < $PWD/docs/examples/barp.d/task_templates/stdin.cfg

Hello, World! There are more arguments will be printed if any provided:  one two three
```

__Composing profile from multiple configuration files:__

_Case 1. Using 'local' profile only:_

```bash
barp run \
    -p $PWD/docs/examples/barp.d/profiles/local.cfg \
    file://$PWD/docs/examples/barp.d/task_templates/command.cfg?command.print_env_vars

BARP_SAMPLE_PROFILE_VAR_A=profile_env_val_env
BARP_SAMPLE_PROFILE_VAR_C=
BARP_SAMPLE_PROFILE_VAR_D=profile_env_val_task
BARP_SAMPLE_TASK_VAR_A=task_test
```

_Case 2. Using 'common' profile is added:_

```bash
barp run \
    -p $PWD/docs/examples/barp.d/profiles/common.cfg:$PWD/docs/examples/barp.d/profiles/local.cfg \
    file://$PWD/docs/examples/barp.d/task_templates/command.cfg?command.print_env_vars

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
$ barp run file://$PWD/docs/examples/barp.d/task_templates/command.cfg?print_env_vars
Here is an env var from task: "test"; Here is an env var from profile: "abc"

# Docker. NB: Docker needs to be running
$ pip intall -e $PWD/docs/examples/plugins/barp_example_executors  # install a plugin to support more envs
$ export BARP_PROFILE=$PWD/docs/examples/barp.d/profiles/docker.cfg
$ barp run file://$PWD/docs/examples/barp.d/task_templates/command.cfg?print_env_vars
Here is an env var from task: "test"; Here is an env var from profile: "abc_docker"

$ pip uninstall barp_example_executors # cleanup
```

## Some ideas for implementation

### Event listeners

Catch events like "before task start", "after task end", etc

### Task transformers

If task template is incompatible with some executor, transformers could convert it into compatible one.
Or it could be trasformation from configuration of other incompatible tool.

### Project management

Combine tasks into projects + compile projects, like Apache Airflow

## Standard library of executors

- Kubernetes job
- SSH
- Python file