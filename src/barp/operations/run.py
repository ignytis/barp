from configtpl.config_builder import ConfigBuilder
from configtpl.utils.dicts import dict_deep_merge

from barp.system import SystemCommand, system_run_command

error_template_path_fmt = "Template path should be in format 'path_to_file:task_template_id'e.g. /tmp/tasks.cfg:my_task"
error_template_id_not_found = "Task template with `{id}` not found in file `{path}`"


def run(template_path: str, additional_args: list[str], profile_path: str) -> None:
    """Runs a process"""
    cfg_builder = ConfigBuilder()
    profile = cfg_builder.build_from_files(profile_path)

    template_path_parts = template_path.rsplit(":", 1)
    if len(template_path_parts) != 2:  # noqa: PLR2004 2 is not a magic value
        raise ValueError(error_template_path_fmt)

    template_file, template_id = template_path_parts
    template_file_rendered = cfg_builder.build_from_files(template_file)
    template = template_file_rendered.get(template_id)
    if template is None:
        raise ValueError(error_template_id_not_found.format(id=template_id, path=template_file))

    # merge task defaults from profile into template
    if "task_defaults" in profile:
        template = dict_deep_merge(template, profile["task_defaults"])
        del profile["task_defaults"]

    cmd = SystemCommand(args=template.get("args", []), env=template.get("env", {}))
    cmd.args += additional_args

    system_run_command(cmd)
