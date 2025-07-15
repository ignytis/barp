import logging
import os
import subprocess
import threading

from barp.executors.base import BaseExecutor
from barp.types.environments.base import BaseEnvironment
from barp.types.environments.local import LocalEnvironment
from barp.types.tasks.base import BaseTaskTemplate
from barp.types.tasks.system_command import SystemCommandTaskTemplate


class LocalExecutor(BaseExecutor):
    """Executes system commands locally"""

    @classmethod
    def supports(cls, environment: BaseEnvironment, task_template: BaseTaskTemplate) -> bool:
        """Returns True if a system command executes in local environment"""
        return type(environment) is LocalEnvironment and type(task_template) is SystemCommandTaskTemplate

    def execute(self, task_template: SystemCommandTaskTemplate, additional_args: list[str]) -> None:
        """Executes the task from template"""
        profile_env: LocalEnvironment = self.profile.environment
        process = subprocess.Popen(
            args=task_template.args + additional_args,
            env={**(os.environ if profile_env.env_passthrough else {}), **profile_env.env, **task_template.env},
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            text=True,
        )

        def print_output() -> None:
            for line in process.stdout:
                print(line, end="")  # noqa: T201 allowing the print statement

        try:
            t = threading.Thread(target=print_output)
            t.start()
            while t.is_alive():
                t.join(timeout=0.1)
        except KeyboardInterrupt:
            logger = logging.getLogger(__name__)
            logger.info("Ctrl+C detected! Terminating the process...")
            process.terminate()
            process.wait()
        finally:
            process.stdout.close()
            process.wait()
