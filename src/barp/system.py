import logging
import subprocess
import threading
from dataclasses import dataclass, field


@dataclass
class SystemCommand:
    """Stores payload for system command"""

    args: list[str]
    """Aeguments e.g. ['ls', '-l']"""
    env: dict[str, str] | None = field(default_factory=dict)
    """Environment variables for system command"""


def system_run_command(command: SystemCommand) -> None:
    """Runs a system command"""
    process = subprocess.Popen(
        args=command.args,
        env=command.env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=1,
        text=True,
    )

    def print_output() -> None:
        for line in process.stdout:
            print(line, end="")  # noqa: T201 allowing the print statement

    try:
        t = threading.Thread(target=print_output)
        t.start()
        while t.is_alive():
            t.join(timeout=0.1)
    except KeyboardInterrupt:
        logger = logging.getLogger(__name__)
        logger.info("Ctrl+C detected! Terminating the process...")
        process.terminate()
        process.wait()
    finally:
        process.stdout.close()
        process.wait()
