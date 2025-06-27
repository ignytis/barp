from barp.arg_builders.base import BaseArgBuilder
from barp.system import SystemCommand


class SystemCommandArgBuilder(BaseArgBuilder):
    """A builder for system command"""

    @staticmethod
    def supports_task_kind(kind: str) -> bool:
        """Return True if task kind is command"""
        return kind == "command"

    def build(self, task_template: dict, args: list) -> SystemCommand:
        """Builds arguments for system command"""
        cmd = SystemCommand(args=task_template.get("args", []), env=task_template.get("env", {}))
        cmd.args.extend(args)
        return cmd
