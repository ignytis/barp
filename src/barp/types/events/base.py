class BaseEvent:
    """Base class for events"""

    def __init__(self) -> None:
        self._is_propagation_enabled: bool = True

    def stop_propagation(self) -> None:
        """Stops event propagation"""
        self._is_propagation_enabled = False

    @property
    def is_propagation_enabled(self) -> bool:
        """If True, event listeners keep processing this event"""
        return self._is_propagation_enabled
