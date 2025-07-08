from enum import Enum
from typing import Literal

from pydantic import Field

from barp.types.models import BaseStrictModel
from barp.types.tasks.command import CommandTaskTemplate


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


class DockerTaskTemplate(CommandTaskTemplate):
    """
    Task template for Docker containers.

    Derives from command task template, because also contains the environment variables
    """

    kind: Literal["docker"] = "docker"

    image: str
    """Image to use"""
    volumes: list[DockerEnvironmentVolume] = Field(default_factory=list)
    """Volumes to mount"""
