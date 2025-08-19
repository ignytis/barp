import logging

import click

from barp.cli.commands.run import cmd_run
from barp.initializer import barp_init

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)


@click.group
def cmd_group_main() -> None:
    """Main command group"""


cmd_group_main.add_command(cmd_run)


if __name__ == "__main__":
    barp_init()
    cmd_group_main()
