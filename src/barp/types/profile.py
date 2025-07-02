from typing import Annotated

from pydantic import BaseModel, ValidatorFunctionWrapHandler, WrapValidator

from barp.models import validate_child_model
from barp.types.environments.base import BaseEnvironment


def _convert_env(v: object, h: ValidatorFunctionWrapHandler) -> BaseEnvironment:
    return h(validate_child_model(v, "barp.types.environments", "kind"))


class Profile(BaseModel):
    """
    Represents the contents of profile configuration file.

    See example: docs/examples/barp.d/profiles/local.cfg
    """

    environment: Annotated[BaseEnvironment, WrapValidator(_convert_env)]
    """Environment configuration"""
    task_defaults: dict
    """Defaults which will be applied to all tasks running with given profile"""
