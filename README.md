# Barp: Build Arguments, Run Process

## Trivia

This application simplifies execution of processes by providing a flexible way to define arguments.

## Status

Early WIP

## Example of execution

```bash
/barp run -t $PWD/docs/examples/task_templates/command.cfg:ls -- /home

total 16K
drwxr-xr-x.  4 root       root       4,0K  9. mai   03:00 .
dr-xr-xr-x. 20 root       root       4,0K 20. mai   00:40 ..
drwx------. 41 user       user       4,0K 25. mai   01:44 user  
```

## FAQ

__Why Rust? The same might be done in Python__

There are few points in favor of Rust:

1. Simplicity of installation. Python will need the interpreter + dependencies to be installed.
   Barp is expected to be a small tool, preferrable a single binary.
1. Golang was considered too as a more simple alternative, but templating and Lua libraries for Rust
   seemed more activaly maintained.

