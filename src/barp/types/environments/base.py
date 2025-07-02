from pydantic import BaseModel


class BaseEnvironment(BaseModel):
    """A base class for environment."""

    kind: str
