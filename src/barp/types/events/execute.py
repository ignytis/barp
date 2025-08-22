from barp.executors.base import BaseExecutor
from barp.types.profile import Profile
from barp.types.tasks.base import BaseTaskTemplate


class TaskExecutionContext:
    """Context of task execution"""

    def __init__(
        self, profile: Profile, executor: BaseExecutor, task_template: BaseTaskTemplate, additional_args: list[str]
    ) -> None:
        super().__init__()
        self.profile = profile
        self.executor = executor
        self.task_template = task_template
        self.additional_args = additional_args
        self.params: dict = {}
