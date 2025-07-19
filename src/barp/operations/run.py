import logging
from typing import TYPE_CHECKING
from urllib.parse import urlparse

from configtpl.config_builder import ConfigBuilder
from configtpl.utils.dicts import dict_deep_merge

from barp.executors.factory import get_executor
from barp.models import validate_child_model
from barp.operations.decorators import barp_operation
from barp.task_template_resolvers.factory import get_task_template_resovler
from barp.types.profile import Profile

if TYPE_CHECKING:
    from barp.types.tasks.base import BaseTaskTemplate

ERROR_PROFILE_NO_ENV_PROVIDED = (
    "No environment configuration is provided in profile.Please add the `environment` section to profile"
)
ERROR_TASK_TPL_RESOLVER_NOT_FOUND = "Task template resolver not found for URL {url}"
ERROR_EXECUTOR_NOT_FOUND = "Cannot find an executor for task kind `{task_kind}` in environment `{env_kind}`"

logger = logging.getLogger(__name__)


@barp_operation
def run(profile_path: str, task_template_url: str, additional_args: list[str] | None = None) -> None:
    """Runs a process"""
    if additional_args is None:
        additional_args = []

    cfg_builder = ConfigBuilder()
    profile = cfg_builder.build_from_files(profile_path)
    profile = Profile.model_validate(profile)
    task_tpl = _get_task_template(task_template_url, profile, cfg_builder)

    if profile.task_defaults is not None:
        task_tpl = dict_deep_merge(profile.task_defaults, task_tpl)

    task_tpl: BaseTaskTemplate = validate_child_model(task_tpl, "barp.types.task_templates", "kind")

    executor = get_executor(profile, task_tpl)
    if executor is None:
        raise ValueError(ERROR_EXECUTOR_NOT_FOUND.format(task_kind=task_tpl.kind, env_kind=profile.environment.kind))

    executor.execute(task_tpl, additional_args)


def _get_task_template(task_template_url: str, profile: dict, cfg_builder: ConfigBuilder) -> dict:
    """Resolves a task template. If no path is provided, returns an empty template"""
    if not task_template_url:
        return {"id": "unnamed"}

    parsed_url = urlparse(task_template_url)
    task_tpl_resolver = get_task_template_resovler(cfg_builder=cfg_builder, profile=profile, url=parsed_url)
    if task_tpl_resolver is None:
        raise RuntimeError(ERROR_TASK_TPL_RESOLVER_NOT_FOUND.format(url=task_template_url))

    return task_tpl_resolver.resolve(parsed_url)
