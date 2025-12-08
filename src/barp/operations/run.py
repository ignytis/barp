import logging
from typing import TYPE_CHECKING, cast
from urllib.parse import urlparse

from configtpl.main import ConfigTpl
from configtpl.utils.dicts import dict_deep_merge
from pydantic import ValidationError

from barp.events.event_dispatcher import dispatch_event
from barp.executors.factory import get_executor
from barp.models import validate_child_model
from barp.task_template_resolvers.factory import get_task_template_resovler
from barp.types.events.execute import TaskExecutionContext
from barp.types.events.post_execute import PostExecuteEvent
from barp.types.events.pre_execute import PreExecuteEvent
from barp.types.profile import Profile

if TYPE_CHECKING:
    from barp.types.tasks.base import BaseTaskTemplate

ERROR_PROFILE_PATH_NOT_PROVIDED = "Profile path is not provided"
ERROR_PROFILE_FORMAT = (
    "Cannot load the profile. Please ensure that environment `{env_kind}` is supported by your current profile "
    "and there are no issues with following fields: {fields}"
)
ERROR_PROFILE_NO_ENV_PROVIDED = (
    "No environment configuration is provided in profile.Please add the `environment` section to profile"
)
ERROR_TASK_TPL_RESOLVER_NOT_FOUND = "Task template resolver not found for URL {url}"
ERROR_EXECUTOR_NOT_FOUND = "Cannot find an executor for task kind `{task_kind}` in environment `{env_kind}`"

logger = logging.getLogger(__name__)


def run(profile_path: str, task_template_url: str, additional_args: list[str] | None = None) -> None:
    """Runs a process"""
    if additional_args is None:
        additional_args = []

    cfg_builder = ConfigTpl()
    if not profile_path:
        raise ValueError(ERROR_PROFILE_PATH_NOT_PROVIDED)
    profile_dict = cfg_builder.build_from_files(paths=[profile_path])
    try:
        profile = Profile.model_validate(profile_dict)
    except ValidationError as e:
        invalid_fields = [".".join(err["loc"]) for err in e.errors()]
        logger.debug("Profile: %s", profile_dict)
        raise RuntimeError(
            ERROR_PROFILE_FORMAT.format(env_kind=profile_dict.get("environment").get("kind"), fields=invalid_fields)
        ) from e

    task_tpl_dict = _get_task_template(task_template_url, profile, cfg_builder)
    if profile.task_defaults is not None:
        task_tpl_dict = dict_deep_merge(profile.task_defaults, task_tpl_dict)
    task_tpl = cast("BaseTaskTemplate", validate_child_model(task_tpl_dict, "barp.types.task_templates", "kind"))

    executor = get_executor(profile, task_tpl)
    if executor is None:
        raise ValueError(ERROR_EXECUTOR_NOT_FOUND.format(task_kind=task_tpl.kind, env_kind=profile.environment.kind))

    ctx = TaskExecutionContext(
        profile=profile, executor=executor, task_template=task_tpl, additional_args=additional_args
    )
    event = PreExecuteEvent(ctx=ctx)
    dispatch_event(event)
    executor.execute(event.ctx.task_template, event.ctx.additional_args)
    dispatch_event(PostExecuteEvent(ctx=ctx))


def _get_task_template(task_template_url: str, profile: Profile, cfg_builder: ConfigTpl) -> dict:
    """Resolves a task template"""
    # If no path is provided, returns an empty template
    if not task_template_url:
        return {"id": "unnamed"}

    parsed_url = urlparse(task_template_url)
    task_tpl_resolver = get_task_template_resovler(cfg_builder=cfg_builder, profile=profile, url=parsed_url)
    if task_tpl_resolver is None:
        raise RuntimeError(ERROR_TASK_TPL_RESOLVER_NOT_FOUND.format(url=task_template_url))

    return task_tpl_resolver.resolve(parsed_url)
