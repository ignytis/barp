from typing import Literal

from pydantic import Field

from barp.types.tasks.base import BaseTaskTemplate


class SystemCommandTaskTemplate(BaseTaskTemplate):
    """Task template for sytem commands"""

    kind: Literal["system_command"] = "system_command"

    args: list[str] = Field(default_factory=list)
    """Command line arguments"""
    env: dict[str, str] = Field(default_factory=dict)
    """Custom environment variables for child process"""
