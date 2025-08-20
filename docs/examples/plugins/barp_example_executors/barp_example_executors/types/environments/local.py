from typing import Literal

from pydantic import Field

from barp.types.environments.base import BaseEnvironment


class LocalEnvironment(BaseEnvironment):
    """Local environment, or a local process"""

    kind: Literal["local"] = "local"

    env: dict[str, str] = Field(default_factory=dict)
    """Profile-specific environment variables"""
    env_passthrough: bool = False
    """If True, environment variables from the app will be passed to child process"""
