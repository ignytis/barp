from typing import Literal

from barp.types.environments.local import LocalEnvironment


class DockerEnvironment(LocalEnvironment):
    """
    A Docker container environment.

    It derives from local enviromnent because it has common features, like env variables.
    """

    kind: Literal["docker"] = "docker"
