import logging

import click

from .commands.run import cmd_run

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)


@click.group
def cmd_group_main() -> None:
    """Main command group"""


cmd_group_main.add_command(cmd_run)


if __name__ == "__main__":
    cmd_group_main()
