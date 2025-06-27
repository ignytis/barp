from abc import ABC, abstractmethod

from barp.system import SystemCommand


class BaseArgBuilder(ABC):
    """A base class for argument builder"""

    def __init__(self, profile: dict) -> None:
        """Create an instance of argument builder for provided profile"""
        self.profile = profile

    @staticmethod
    def supports_task_kind(_kind: str) -> bool:
        """Return True if task with provided kind is supported by this argument builder"""
        return False

    def get_priority(self) -> int:
        """
        Returns a priority for argument builder.

        A higher priority might be specified to override anoter agument builder
        """
        return 0

    @abstractmethod
    def build(self, task_template: dict, args: list) -> SystemCommand:
        """Build the system command arguments for task template"""
        raise NotImplementedError
