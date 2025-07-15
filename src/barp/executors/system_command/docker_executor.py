import logging
import os

from barp.executors.base import BaseExecutor
from barp.types.environments.base import BaseEnvironment
from barp.types.environments.docker import DockerEnvironment
from barp.types.tasks.base import BaseTaskTemplate
from barp.types.tasks.system_command import SystemCommandTaskTemplate

try:
    import docker
except ImportError:
    docker = None


class DockerExecutor(BaseExecutor):
    """Executes system commands in Docker"""

    logger = logging.getLogger(__name__)

    @classmethod
    def supports(cls, environment: BaseEnvironment, task_template: BaseTaskTemplate) -> bool:
        """Returns True if a system command executes in Docker environment"""
        if not (type(environment) is DockerEnvironment and type(task_template) is SystemCommandTaskTemplate):
            return False
        if docker is None:
            cls.logger.warning(
                "The provided task is compatible with Docker, but `env_docker` extra is not installed. "
                "Please install barp with `env_docker` extra to enable support for Docker"
            )
            return False
        return True

    def execute(self, task_template: SystemCommandTaskTemplate, additional_args: list[str]) -> None:
        """Executes the task from template"""
        profile_env: DockerEnvironment = self.profile.environment

        client = docker.from_env(environment={**os.environ, **profile_env.env} if profile_env.env_passthrough else {})

        if profile_env.pull_image:
            self.logger.info("Pulling image %s...", profile_env.image)
            client.images.pull(profile_env.image)

        container = client.containers.run(
            auto_remove=profile_env.auto_remove,
            detach=True,
            command=task_template.args + additional_args,
            image=profile_env.image,
            entrypoint=profile_env.entry_point,
            environment=profile_env.env,
            volumes=[f"{v.host_path}:{v.container_path}:{v.mode}" for v in profile_env.volumes],
        )
        for line in container.logs(stream=True):
            print(line.decode("utf-8"), end="")  # noqa: T201 raw output of logs
