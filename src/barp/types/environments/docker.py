from enum import Enum
from typing import Literal

from pydantic import Field

from barp.types.environments.local import LocalEnvironment
from barp.types.models import BaseStrictModel


class DockerEnvironmentVolumeMountMode(Enum):
    """Volume mounting mode"""

    ro = "ro"
    """Read-only mode"""
    rw = "rw"
    """Read and Write mode"""


class DockerEnvironmentVolume(BaseStrictModel):
    """A volume to mount in Docker container"""

    host_path: str
    """path the host system"""
    container_path: str
    """path inside container"""
    mode: DockerEnvironmentVolumeMountMode = DockerEnvironmentVolumeMountMode.ro


class DockerEnvironment(LocalEnvironment):
    """
    A Docker container environment.

    It derives from local enviromnent because it has common features, like env variables.
    """

    kind: Literal["docker"] = "docker"

    auto_remove: str | None = None
    """Auto remove container after execution. Might be overridden for debug reasons"""
    entry_point: str | None = None
    """Entry point to use"""
    image: str
    """Image to use"""
    pull_image: bool = True
    """Pull image before running"""
    volumes: list[DockerEnvironmentVolume] = Field(default_factory=list)
    """Volumes to mount"""
