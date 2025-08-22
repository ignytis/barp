import click

from barp.operations.run import run


@click.command(
    name="run",
    help="Runs a command. Target is a task template ID and optional execution environment separaterd with '@'",
)
@click.option("--profile", "-p", "profile_path", envvar="BARP_PROFILE", help="Path to file with profile conifg")
@click.argument("task_template_url", required=True)
@click.argument("args", nargs=-1)
def cmd_run(args: tuple[str], task_template_url: str, profile_path: str) -> None:
    """An entry point of 'run' command"""
    run(profile_path, task_template_url, None if args is None else list(args))
