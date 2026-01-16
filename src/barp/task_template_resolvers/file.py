from urllib.parse import ParseResult

from configtpl.main import ConfigTpl

from barp.task_template_resolvers.base import BaseTaskTemplateResolver
from barp.types.models import BaseStrictModel
from barp.types.profile import Profile

ERROR_TEMPLATE_ID_NOT_FOUND = "Task template with `{id}` not found in file `{path}`"


class FileTaskTemplateResolverConfig(BaseStrictModel):
    """Configuration for FileTaskTemplateResolver"""

    file_format: str = "yaml"


class FileTaskTemplateResolver(BaseTaskTemplateResolver):
    """A resolver of file:// URLs. Looks up the provided file and fetches the task ID from query params"""

    config_cls: type[FileTaskTemplateResolverConfig] = FileTaskTemplateResolverConfig

    def __init__(self, cfg_builder: ConfigTpl, profile: Profile) -> None:
        super().__init__(cfg_builder, profile)

    @classmethod
    def supports(cls, url: ParseResult) -> bool:
        """Returns True if URL scheme is file://"""
        return url.scheme == "file"

    def resolve(self, url: ParseResult) -> dict:
        """Resolves the provided local file URL"""
        path = url.path
        template_id = url.query
        template_file_rendered = self.cfg_builder.build_from_files(
            paths=[path], ctx={"profile": self.profile}, file_type=self.config.file_format
        )
        task_tpl = template_file_rendered.get(template_id)
        if task_tpl is None:
            raise ValueError(ERROR_TEMPLATE_ID_NOT_FOUND.format(id=template_id, path=path))
        task_tpl["id"] = template_id

        return task_tpl

    @classmethod
    def get_priority(cls) -> int:
        """Returns a priority."""
        return 0
