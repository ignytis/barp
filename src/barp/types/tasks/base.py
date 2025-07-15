from pydantic import Field

from barp.types.models import BaseStrictModel


class BaseTaskTemplate(BaseStrictModel):
    """A base class for task templates."""

    id: str = Field(pattern="[a-zA-Z0-9-._]+")
    """A unique identifier for the task template"""

    kind: str
    """A discriminator which defines the kind of task template"""
