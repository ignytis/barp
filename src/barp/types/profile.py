from pydantic import BaseModel

from barp.types.environments.base import BaseEnvironment


class Profile(BaseModel):
    """
    Represents the contents of profile configuration file.

    See example: docs/examples/barp.d/profiles/local.cfg
    """

    environment: BaseEnvironment
    """Environment configuration"""
    task_defaults: dict
    """Defaults which will be applied to all tasks running with given profile"""
