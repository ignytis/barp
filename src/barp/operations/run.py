from configtpl.config_builder import ConfigBuilder

from barp.system import system_run_command

error_template_path_fmt = "Template path should be in format 'path_to_file:task_template_id'e.g. /tmp/tasks.cfg:my_task"
error_template_id_not_found = "Task template with `{id}` not found in file `{path}`"


def run(template_path: str, additional_args: list[str], profile_path: str) -> None:
    """Runs a process"""
    cfg_builder = ConfigBuilder()
    profile = cfg_builder.build_from_files(profile_path)

    template_path_parts = template_path.split(":")
    if len(template_path_parts) != 2:  # noqa: PLR2004 2 is not a magic value
        raise ValueError(error_template_path_fmt)

    template_file, template_id = template_path_parts
    template_file_rendered = cfg_builder.build_from_files(template_file)
    template = template_file_rendered.get(template_id)
    if template is None:
        raise ValueError(error_template_id_not_found.format(id=template_id, path=template_file))

    template = {**template, **profile.get("task_defaults", {})}

    args = template.get("args", [])
    args += additional_args
    env = template.get("env", {})

    system_run_command(args=args, env=env)
