import logging
import os
from functools import wraps


def barp_operation(func: callable) -> callable:
    """All Barp operators should use this decorator"""

    @wraps(func)
    def initialized_operation(*args: list, **kwargs: dict) -> any:
        _init_logger()

        """Initialized Barp and runs the original function"""
        return func(*args, **kwargs)

    return initialized_operation


def _init_logger() -> None:
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(
        format="%(asctime)s PID %(process)d [%(levelname)s] %(name)s: %(message)s",
        level=log_level,
    )
    logging.getLogger("barp").setLevel(log_level)
