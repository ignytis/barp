# Barp: Build Arguments, Run Process

## Trivia

This application simplifies execution of processes by providing a flexible way to define arguments.

## Status

Early WIP

## Example of execution

```bash
$ barp run -p $PWD/docs/examples/barp.d/profiles/local.cfg -t $PWD/docs/examples/barp.d/task_templates/command.cfg:print_n_times
Hello 1 🚀
Hello 2 🚀
Hello 3 🚀
Hello 4 🚀
Hello 5 🚀
Example error! 💥
Process exited with code 0
```

## FAQ

__Why Rust? The same might be done in Python__

There are few points in favor of Rust:

1. Simplicity of installation. Python will need the interpreter + dependencies to be installed.
   Barp is expected to be a small tool, preferrable a single binary.
1. Golang was considered too as a more simple alternative, but templating and Lua libraries for Rust
   seemed more activaly maintained.

