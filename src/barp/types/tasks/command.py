from typing import Literal

from pydantic import Field

from barp.types.tasks.base import BaseTaskTemplate


class CommandTaskTemplate(BaseTaskTemplate):
    """Task template for sytem commands"""

    kind: Literal["command"] = "command"

    args: list[str] = Field(default_factory=list)
    """Command line arguments"""
    env: dict[str, str] = Field(default_factory=dict)
    """Custom environment variables for child process"""
