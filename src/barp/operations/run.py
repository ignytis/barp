from configtpl.config_builder import ConfigBuilder
from configtpl.utils.dicts import dict_deep_merge

from barp.arg_builders.factory import arg_builder_find_by_task_kind
from barp.system import system_run_command

ERROR_TEMPLATE_PATH_FMT = "Template path should be in format 'path_to_file:task_template_id'e.g. /tmp/tasks.cfg:my_task"
ERROR_TEMPLATE_ID_NOT_FOUND = "Task template with `{id}` not found in file `{path}`"
ERROR_TASK_KIND_MISING = "Task kind is not provided in template. Please add the 'kind' attribute"
ERROR_ARG_BUILDER_NOT_FOUND = "Argument builder not found for task kind: {task_kind}"


def run(template_path: str, additional_args: list[str], profile_path: str) -> None:
    """Runs a process"""
    cfg_builder = ConfigBuilder()
    profile = cfg_builder.build_from_files(profile_path)

    template_path_parts = template_path.rsplit(":", 1)
    if len(template_path_parts) != 2:  # noqa: PLR2004 2 is not a magic value
        raise ValueError(ERROR_TEMPLATE_PATH_FMT)

    template_file, template_id = template_path_parts
    template_file_rendered = cfg_builder.build_from_files(template_file)
    template = template_file_rendered.get(template_id)
    if template is None:
        raise ValueError(ERROR_TEMPLATE_ID_NOT_FOUND.format(id=template_id, path=template_file))

    # merge task defaults from profile into template
    if "task_defaults" in profile:
        template = dict_deep_merge(profile["task_defaults"], template)
        del profile["task_defaults"]

    task_kind = template.get("kind")
    if task_kind is None:
        raise ValueError(ERROR_TASK_KIND_MISING)

    arg_builder = arg_builder_find_by_task_kind(task_kind, profile)
    if arg_builder is None:
        raise RuntimeError(ERROR_ARG_BUILDER_NOT_FOUND.format(task_kind=task_kind))
    cmd = arg_builder.build(template, additional_args)

    system_run_command(cmd)
