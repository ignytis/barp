import logging
from typing import TYPE_CHECKING

from configtpl.config_builder import ConfigBuilder
from configtpl.utils.dicts import dict_deep_merge

from barp.executors.factory import get_executor
from barp.models import validate_child_model
from barp.operations.decorators import barp_operation
from barp.types.profile import Profile

if TYPE_CHECKING:
    from barp.types.tasks.base import BaseTaskTemplate

ERROR_PROFILE_NO_ENV_PROVIDED = (
    "No environment configuration is provided in profile.Please add the `environment` section to profile"
)
ERROR_TEMPLATE_PATH_FMT = "Template path should be in format 'path_to_file:task_template_id'e.g. /tmp/tasks.cfg:my_task"
ERROR_TEMPLATE_ID_NOT_FOUND = "Task template with `{id}` not found in file `{path}`"
ERROR_TASK_KIND_MISING = "Task kind is not provided in template. Please add the 'kind' attribute"
ERROR_EXECUTOR_NOT_FOUND = "Cannot find an executor for task kind `{task_kind}` in environment `{env_kind}`"

logger = logging.getLogger(__name__)


@barp_operation
def run(template_path: str, additional_args: list[str], profile_path: str) -> None:
    """Runs a process"""
    cfg_builder = ConfigBuilder()
    profile = cfg_builder.build_from_files(profile_path)
    profile = Profile.model_validate(profile)

    template_path_parts = template_path.rsplit(":", 1)
    if len(template_path_parts) != 2:  # noqa: PLR2004 2 is not a magic value
        raise ValueError(ERROR_TEMPLATE_PATH_FMT)

    template_file, template_id = template_path_parts
    # TODO: apply profile. Need a new ConfigBuilder?
    template_file_rendered = cfg_builder.build_from_files(template_file)
    task_tpl = template_file_rendered.get(template_id)
    if task_tpl is None:
        raise ValueError(ERROR_TEMPLATE_ID_NOT_FOUND.format(id=template_id, path=template_file))

    if profile.task_defaults is not None:
        task_tpl = dict_deep_merge(profile.task_defaults, task_tpl)

    task_tpl: BaseTaskTemplate = validate_child_model(task_tpl, "barp.types.task_templates", "kind")

    executor = get_executor(profile, task_tpl)
    if executor is None:
        raise ValueError(ERROR_EXECUTOR_NOT_FOUND.format(task_kind=task_tpl.kind, env_kind=profile.environment.kind))

    executor.execute(task_tpl, additional_args)
