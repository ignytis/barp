from urllib.parse import ParseResult

from barp.task_template_resolvers.base import BaseTaskTemplateResolver
from barp.types.tasks.base import BaseTaskTemplate

ERROR_TEMPLATE_ID_NOT_FOUND = "Task template with `{id}` not found in file `{path}`"


class FileTaskTemplateResolver(BaseTaskTemplateResolver):
    """A resolver of file:// URLs. Looks up the provided file and fetches the task ID from query params"""

    @classmethod
    def supports(cls, url: ParseResult) -> bool:
        """Returns True if URL scheme is file://"""
        return url.scheme == "file"

    def resolve(self, url: ParseResult) -> BaseTaskTemplate:
        """Resolves the provided local file URL"""
        path = url.path
        template_id = url.query
        template_file_rendered = self.cfg_builder.build_from_files(path, ctx={"profile": self.profile})
        task_tpl = template_file_rendered.get(template_id)
        if task_tpl is None:
            raise ValueError(ERROR_TEMPLATE_ID_NOT_FOUND.format(id=template_id, path=path))
        task_tpl["id"] = template_id

        return task_tpl

    @classmethod
    def get_priority(cls) -> int:
        """Returns a priority."""
        return 0
