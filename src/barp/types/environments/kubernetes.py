from typing import Literal

from barp.types.environments.local import LocalEnvironment


class KubernetesEnvironment(LocalEnvironment):
    """
    A Kubernetes job environment.

    It derives from local enviromnent because it has common features, like env variables.
    """

    kind: Literal["kubernetes"] = "kubernetes"

    image: str
    """Image to use"""

    namespace: str = "default"
    """Kubernetes namespace"""
