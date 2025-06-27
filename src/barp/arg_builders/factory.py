from importlib.metadata import entry_points

from barp.arg_builders.base import BaseArgBuilder
from barp.reflection import reflection_load_class_from_string


def arg_builder_find_by_task_kind(kind: str, profile: dict) -> BaseArgBuilder | None:
    """Locate an argument builder by task kind"""
    arg_builder_classes: list[type[BaseArgBuilder]] = [
        reflection_load_class_from_string(ep.value) for ep in entry_points(group="barp.arg_builders")
    ]
    arg_builder_classes = [x for x in arg_builder_classes if x.supports_task_kind(kind)]
    if not arg_builder_classes:
        return None
    arg_builder_classes = sorted(arg_builder_classes, key=lambda x: x.get_priority, reverse=True)

    return arg_builder_classes[0](profile=profile)
