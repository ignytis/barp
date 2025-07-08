from barp.types.models import BaseStrictModel


class BaseEnvironment(BaseStrictModel):
    """A base class for environment."""

    kind: str
