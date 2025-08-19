from barp.events.listeners.base import BaseEventListener
from barp.types.events.pre_execute import PreExecuteEvent
from barp.types.tasks.system_command import SystemCommandTaskTemplate


class PreExecuteEventListener(BaseEventListener):
    """An example of event listener which adjust the task parameters before execution"""

    event_cls = PreExecuteEvent

    def handle(self, event: PreExecuteEvent) -> None:
        """Handles the pre-execute event"""
        if isinstance(event.ctx.task_template, SystemCommandTaskTemplate):
            event.ctx.task_template.args = ["echo", "Hello from pre-execute listener"]
