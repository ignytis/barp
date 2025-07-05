import os

from barp.executors.base import BaseExecutor
from barp.system import SystemCommand, system_run_command
from barp.types.environments.base import BaseEnvironment
from barp.types.environments.local import LocalEnvironment
from barp.types.tasks.base import BaseTaskTemplate
from barp.types.tasks.command import CommandTaskTemplate


class LocalExecutor(BaseExecutor):
    """Executes tasks locally"""

    @classmethod
    def supports(cls, environment: BaseEnvironment, task_template: BaseTaskTemplate) -> bool:
        """Returns True if a system command executes in local environment"""
        return isinstance(environment, LocalEnvironment) and isinstance(task_template, CommandTaskTemplate)

    def execute(self, task_template: CommandTaskTemplate, additional_args: list[str]) -> None:
        """Executes the task from template"""
        profile_env: LocalEnvironment = self.profile.environment
        env = {**(os.environ if profile_env.env_passthrough else {}), **profile_env.env, **task_template.env}

        cmd = SystemCommand(args=task_template.args + additional_args, env=env)
        system_run_command(cmd)
