# Event listeners

Event listeners can execute custom code on different stages of Barp execution.
Here is an example of adding an event listener which replaces the arguments for system command:

_No listeners. The program uses arguments from configuration_
```bash
$ barp run file://$PWD/docs/examples/barp.d/task_templates/command.cfg?command.print_profile_vars
Hello from `my_lovely_deployment` deployment at `us` region
```

_Now installing a plugin with event listener:_
```bash
$ pip install -e ./docs/examples/plugins/event_listeners/example_listener/
```

_Running the command again. Instead of original arguments the task prints something different:_

```bash
$ barp run file://$PWD/docs/examples/barp.d/task_templates/command.cfg?command.print_profile_vars
Hello from pre-execute listener
```

_Clean-up_

```bash
$ pip uninstall example_listener
```