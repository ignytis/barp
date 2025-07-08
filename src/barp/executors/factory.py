from importlib.metadata import entry_points

from barp.executors.base import BaseExecutor
from barp.reflection import reflection_load_class_from_string
from barp.types.profile import Profile
from barp.types.tasks.base import BaseTaskTemplate


def get_executor(profile: Profile, task_tpl: BaseTaskTemplate) -> BaseExecutor | None:
    """Locate an argument builder by task kind"""
    executor_classes: list[type[BaseExecutor]] = [
        reflection_load_class_from_string(ep.value) for ep in entry_points(group="barp.executors")
    ]
    executor_classes = [x for x in executor_classes if x.supports(profile.environment, task_tpl)]
    if not executor_classes:
        return None
    executor_classes = sorted(executor_classes, key=lambda x: x.get_priority(), reverse=True)

    return executor_classes[0](profile=profile)
