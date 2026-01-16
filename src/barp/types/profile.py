from typing import Annotated

from pydantic import Field, ValidatorFunctionWrapHandler, WrapValidator

from barp.models import validate_child_model
from barp.types.environments.base import BaseEnvironment
from barp.types.models import BaseStrictModel


def _convert_env(v: dict, h: ValidatorFunctionWrapHandler) -> BaseEnvironment:
    return h(validate_child_model(v, "barp.types.environments", "kind"))


class Profile(BaseStrictModel):
    """
    Represents the contents of profile configuration file.

    See example: docs/examples/barp.d/profiles/local.cfg
    """

    environment: Annotated[BaseEnvironment, WrapValidator(_convert_env)]
    """Environment configuration"""
    name: str
    """Profile name"""
    task_defaults: dict = Field(default_factory=dict)
    """Defaults which will be applied to all tasks running with given profile"""
    task_template_resolvers: dict = Field(default_factory=dict)
    """Task template resolvers configuration"""
    vars: dict = Field(default_factory=dict)
    """Custom variables which could be used in task definitions"""
