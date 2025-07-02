from pydantic import BaseModel


class BaseTaskTemplate(BaseModel):
    """A base class for task templates."""

    kind: str
