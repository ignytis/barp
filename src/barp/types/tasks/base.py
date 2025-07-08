from barp.types.models import BaseStrictModel


class BaseTaskTemplate(BaseStrictModel):
    """A base class for task templates."""

    kind: str
