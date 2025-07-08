import abc

from barp.types.environments.base import BaseEnvironment
from barp.types.profile import Profile
from barp.types.tasks.base import BaseTaskTemplate


class BaseExecutor(abc.ABC):
    """A base class for task executors"""

    def __init__(self, profile: Profile) -> None:
        """Initializes an instance of executor based on profile"""
        self.profile = profile

    @classmethod
    @abc.abstractmethod
    def supports(cls, environment: BaseEnvironment, task_template: BaseTaskTemplate) -> bool:
        """
        Checks compatibility with environment and task template.

        Returns True if the current implementation of executor supports execution
        of provided task template in particular environment
        """
        raise NotImplementedError

    def execute(self, task_template: BaseTaskTemplate, additional_args: list[str]) -> None:
        """Executes the task from template"""
        raise NotImplementedError

    @classmethod
    def get_priority(cls) -> int:
        """
        Returns a priority.

        A higher priority might be specified to override anoter executor
        """
        return 0
