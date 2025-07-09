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

        if task_template.pull_image:
            self.logger.info("Pulling image %s...", task_template.image)
            client.images.pull(task_template.image)

        container = client.containers.run(
            auto_remove=task_template.auto_remove,
            detach=True,
            command=task_template.args + additional_args,
            image=task_template.image,
            entrypoint=task_template.entry_point,
            environment=task_template.env,
            volumes=[f"{v.host_path}:{v.container_path}:{v.mode}" for v in task_template.volumes],
        )
        for line in container.logs(stream=True):
            print(line.decode("utf-8"), end="")  # noqa: T201 raw output of logs
