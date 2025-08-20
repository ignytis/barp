from pydantic import BaseModel, ConfigDict


class BaseStrictModel(BaseModel):
    """
    A base class for models which disallows extra values and uses values of enums.

    It's encouraged to use this class to fail fast in case of misformatted config.
    """

    model_config = ConfigDict(extra="forbid", use_enum_values=True)
