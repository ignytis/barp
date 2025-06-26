import click

from barp.operations.run import run


@click.command(
    name="run",
    help="Runs a command. Target is a task template ID and optional execution environment separaterd with '@'",
)
@click.option("--profile", "-p", "profile_path", envvar="BARP_PROFILE", help="Path to file with profile conifg")
@click.option("--template", "-t", "template_path", help="Path to task template e.g. /test/example.yaml:my_task")
@click.argument("args", nargs=-1)
def cmd_run(template_path: str, args: tuple[str], profile_path: str | None = None) -> None:
    """An entry point of 'run' command"""
    run(template_path, list(args), profile_path)
