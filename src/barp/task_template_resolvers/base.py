import abc
from urllib.parse import ParseResult

from configtpl.config_builder import ConfigBuilder

from barp.types.profile import Profile
from barp.types.tasks.base import BaseTaskTemplate


class BaseTaskTemplateResolver(abc.ABC):
    """A base class for task template resolvers"""

    def __init__(self, cfg_builder: ConfigBuilder, profile: Profile) -> None:
        """Creates ann instance of Task Template Resolver"""
        self.cfg_builder = cfg_builder
        self.profile = profile

    @classmethod
    @abc.abstractmethod
    def supports(cls, url: ParseResult) -> bool:
        """
        Checks if the resolver supports the provided URL.

        Returns True if the current implementation of resolver supports the provided URL
        """
        raise NotImplementedError

    def resolve(self, url: ParseResult) -> BaseTaskTemplate:
        """Resolves the provided URL"""
        raise NotImplementedError

    @classmethod
    def get_priority(cls) -> int:
        """
        Returns a priority.

        A higher priority might be specified to override anoter resolver
        """
        return 0
