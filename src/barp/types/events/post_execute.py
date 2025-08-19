from barp.types.events.base import BaseEvent
from barp.types.events.execute import TaskExecutionContext


class PostExecuteEvent(BaseEvent):
    """Triggered after task execution"""

    def __init__(self, ctx: TaskExecutionContext) -> None:
        super().__init__()
        self.ctx = ctx
