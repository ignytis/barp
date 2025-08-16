from barp.events.listeners.base import BaseEventListener
from barp.types.events.base import BaseEvent

_listeners: dict[type[BaseEvent], list[BaseEventListener]] = {}


def register_event_listener(event_cls: type[BaseEvent], listener: BaseEventListener) -> None:
    """Registers event listener in the module"""
    global _listeners  # noqa: PLW0602
    if event_cls not in _listeners:
        _listeners[event_cls] = []
    _listeners[event_cls].append(listener)


def dispatch_event(event: BaseEvent) -> None:
    """Processes an event. Passes the event to corresponding listeners"""
    global _listeners  # noqa: PLW0602
    event_cls = event.__class__
    if event_cls not in _listeners:  # no event in listeners means that no listeners is registered for provided event
        return
    for listener in _listeners[event_cls]:
        if not event.is_propagation_enabled:
            break
        listener.handle(event)
