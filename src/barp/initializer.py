import logging
import os
from importlib.metadata import entry_points
from typing import TYPE_CHECKING, cast

from barp.events.event_dispatcher import register_event_listener
from barp.reflection import reflection_load_class_from_string

if TYPE_CHECKING:
    from barp.events.listeners.base import BaseEventListener
    from barp.types.events.base import BaseEvent


def barp_init() -> None:
    """Initializes the library. All entry points (CLI components or server initalization routines) should call this"""
    _init_logger()
    _register_event_listeners()


def _init_logger() -> None:
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(
        format="%(asctime)s PID %(process)d [%(levelname)s] %(name)s: %(message)s",
        level=log_level,
    )
    logging.getLogger("barp").setLevel(log_level)


def _register_event_listeners() -> None:
    event_listener_classes = cast(
        "list[type[BaseEventListener]]",
        [reflection_load_class_from_string(ep.value) for ep in entry_points(group="barp.event_listeners")],
    )

    # Create an instance of event listener per event listener class and sort listeners by priority for each event type
    event_classes = cast("list[type[BaseEvent]]", {listener_cls.event_cls for listener_cls in event_listener_classes})
    event_listeners_map: dict[type[BaseEvent], list[BaseEventListener]] = {
        event_class: [] for event_class in event_classes
    }
    for event_listener_class in event_listener_classes:
        event_listeners_map[event_listener_class.event_cls].append(event_listener_class())
    event_listeners_map = {
        event_cls: sorted(event_listeners, key=lambda x: x.get_priority(), reverse=True)
        for event_cls, event_listeners in event_listeners_map.items()
    }

    for event_listener_class in event_listener_classes:
        register_event_listener(event_listener_class.event_cls, event_listener_class())
