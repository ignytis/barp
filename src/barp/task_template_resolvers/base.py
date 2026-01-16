import abc
from urllib.parse import ParseResult

from configtpl.main import ConfigTpl

from barp.reflection import reflection_format_class_path_for_class
from barp.types.models import BaseStrictModel
from barp.types.profile import Profile


class BaseTaskTemplateResolver(abc.ABC):
    """A base class for task template resolvers"""

    config_cls: type[BaseStrictModel] = BaseStrictModel

    def __init__(self, cfg_builder: ConfigTpl, profile: Profile) -> None:
        """Creates ann instance of Task Template Resolver"""
        self.cfg_builder = cfg_builder
        self.profile = profile

        task_resolver_class_path = reflection_format_class_path_for_class(self.__class__)
        cfg = profile.task_template_resolvers.get(task_resolver_class_path)
        self.config = self.__class__.config_cls.model_validate({} if cfg is None else cfg)

    @classmethod
    @abc.abstractmethod
    def supports(cls, url: ParseResult) -> bool:
        """
        Checks if the resolver supports the provided URL.

        Returns True if the current implementation of resolver supports the provided URL
        """
        raise NotImplementedError

    def resolve(self, url: ParseResult) -> dict:
        """Resolves the provided URL"""
        raise NotImplementedError

    @classmethod
    def get_priority(cls) -> int:
        """
        Returns a priority.

        A higher priority might be specified to override anoter resolver
        """
        return 0
