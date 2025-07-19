from importlib.metadata import entry_points
from urllib.parse import ParseResult

from configtpl.config_builder import ConfigBuilder

from barp.reflection import reflection_load_class_from_string
from barp.task_template_resolvers.base import BaseTaskTemplateResolver
from barp.types.profile import Profile


def get_task_template_resovler(
    cfg_builder: ConfigBuilder, profile: Profile, url: ParseResult
) -> BaseTaskTemplateResolver | None:
    """Locate a task template resolver by task URL"""
    resolver_classes: list[type[BaseTaskTemplateResolver]] = [
        reflection_load_class_from_string(ep.value) for ep in entry_points(group="barp.task_template_resolvers")
    ]
    resolver_classes = [x for x in resolver_classes if x.supports(url)]
    if not resolver_classes:
        return None
    resolver_classes = sorted(resolver_classes, key=lambda x: x.get_priority(), reverse=True)

    return resolver_classes[0](profile=profile, cfg_builder=cfg_builder)
