import logging
from importlib.metadata import entry_points
from typing import Annotated, Union

from pydantic import BaseModel, Discriminator, TypeAdapter

ERR_NO_CHILDREN_CLASSES_FOUND = "No children classes found in entry point group {entry_point_group}"
ERR_ENTRY_POINT_LOAD = "Failed to load module `{name}`. Please check the class references in entry points"

logger = logging.getLogger(__name__)


def validate_child_model(d: dict, entry_point_group: str, discriminator: str) -> BaseModel:
    """Returns a derived model of base model T using entrypoints"""
    try:
        children_classes: list[type[BaseModel]] = [ep.load() for ep in entry_points(group=entry_point_group)]
    except ModuleNotFoundError as e:
        logger.exception(ERR_ENTRY_POINT_LOAD.format(name=e.name))
        raise

    if not children_classes:
        raise RuntimeError(ERR_NO_CHILDREN_CLASSES_FOUND.format(entry_point_group=entry_point_group))

    if len(children_classes) == 1:
        return TypeAdapter(children_classes[0]).validate_python(d)

    type_adapter_arg = (
        children_classes[0]
        if len(children_classes) == 1
        else Annotated[Union[*children_classes], Discriminator(discriminator)]
    )

    return TypeAdapter(type_adapter_arg).validate_python(d)
