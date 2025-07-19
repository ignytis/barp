import sys
from urllib.parse import ParseResult

from barp.task_template_resolvers.base import BaseTaskTemplateResolver
from barp.types.tasks.base import BaseTaskTemplate


class StdinTaskTemplateResolver(BaseTaskTemplateResolver):
    """A resolver for standard input. Handles `stdin://` or `-` kind of URLs"""

    @classmethod
    def supports(cls, url: ParseResult) -> bool:
        """Returns True if URL scheme is file://"""
        return url.scheme == "stdin" or (
            url.path == "-"
            and url.scheme == ""
            and url.netloc == ""
            and url.params == ""
            and url.query == ""
            and url.fragment == ""
        )

    def resolve(self, _url: ParseResult) -> BaseTaskTemplate:
        """Resolves the provided local file URL"""
        content = "".join(sys.stdin)
        tpl = self.cfg_builder.build_from_str(content, ctx={"profile": self.profile})
        tpl["id"] = "_stdin"

        return tpl

    @classmethod
    def get_priority(cls) -> int:
        """Returns a priority."""
        return 0
