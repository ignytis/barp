import logging
import time

from barp.events.listeners.base import BaseEventListener
from barp.types.events.post_execute import PostExecuteEvent
from barp.types.events.pre_execute import PreExecuteEvent


class PreExecuteEventListener(BaseEventListener):
    """An example of event listener which logs the execution start time"""

    event_cls = PreExecuteEvent

    def handle(self, event: PreExecuteEvent) -> None:
        """Handles the pre-execute event"""
        event.ctx.params["start_time"] = time.time()

    def get_priority(self) -> int:
        """Returns the priority of the listener"""
        return 100


class PostExecuteEventListener(BaseEventListener):
    """An example of event listener which prints the task execution time"""

    event_cls = PostExecuteEvent
    logger = logging.getLogger(__name__)

    def handle(self, event: PreExecuteEvent) -> None:
        """Handles the pre-execute event"""
        start_time = event.ctx.params["start_time"]
        end_time = time.time()
        duration = end_time - start_time
        self.logger.info("Task duration: %s", duration)

    def get_priority(self) -> int:
        """Returns the priority of the listener"""
        return 100
