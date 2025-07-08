import logging
import os

from barp.executors.base import BaseExecutor
from barp.types.environments.base import BaseEnvironment
from barp.types.environments.docker import DockerEnvironment
from barp.types.tasks.base import BaseTaskTemplate
from barp.types.tasks.docker import DockerTaskTemplate

try:
    import docker
except ImportError:
    docker = None


class DockerCommandExecutor(BaseExecutor):
    """Executes system commands in Docker"""

    logger = logging.getLogger(__name__)

    @classmethod
    def supports(cls, environment: BaseEnvironment, task_template: BaseTaskTemplate) -> bool:
        """Returns True if a system command executes in local environment"""
        if not (type(environment) is DockerEnvironment and type(task_template) is DockerTaskTemplate):
            return False
        if docker is None:
            cls.logger.warning(
                "The provided task is compatible with Docker, but `env_docker` extra is not installed. "
                "Please install barp with `env_docker` extra to enable support for Docker"
            )
            return False
        return True

    def execute(self, task_template: DockerTaskTemplate, additional_args: list[str]) -> None:
        """Executes the task from template"""
        profile_env: DockerEnvironment = self.profile.environment

        client = docker.from_env(environment={**os.environ, **profile_env.env} if profile_env.env_passthrough else {})

        container = client.containers.run(
            auto_remove=True,
            detach=True,
            command=task_template.args + additional_args,
            image=task_template.image,
            entrypoint=None,
            environment=task_template.env,
        )
        for line in container.logs(stream=True):
            print(line.decode("utf-8"), end="")  # noqa: T201 raw output of logs
