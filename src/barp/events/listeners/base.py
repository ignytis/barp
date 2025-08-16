from abc import ABC, abstractmethod

from barp.types.events.base import BaseEvent


class BaseEventListener(ABC):
    """A base class for event listeners"""

    event_cls: type[BaseEvent]
    """Class of event to handle"""

    @abstractmethod
    def handle(self, event: BaseEvent) -> None:
        """Handles an event"""
        raise NotImplementedError

    @classmethod
    def get_priority(cls) -> int:
        """Returns a priority."""
        return 0
