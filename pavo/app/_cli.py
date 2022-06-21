import sys
import argparse

from pavo.ddl.commands import CommandInterface
from pavo.core import messages

from ._app import command_manager
from ._version import has_matching_versions


def _create_argument_parser(
    commands: list[CommandInterface],
) -> argparse.ArgumentParser:
    """Creates an argument parser with recursively added subparsers based on a list of commands.

    Args:
        commands: The commands that should get their own subparser. Highly recommended for all commands.

    Returns:
        The argument parser with subparsers attached.
    """
    argument_parser = argparse.ArgumentParser(
        conflict_handler="resolve", allow_abbrev=False
    )
    subparsers = argument_parser.add_subparsers(dest="command")

    for command in commands:
        command_parser = subparsers.add_parser(command.name)
        command.setup_parser(command_parser)

    return argument_parser


def run_console_application() -> None:
    """Runs Pavo as console application. Used as entry point for console scripts."""
    if not has_matching_versions():
        messages.warning(
            "Your Pavo config file version does not match your actual Pavo version."
        )

    parser = _create_argument_parser([command for (name, command) in command_manager])
    parsed_arguments = parser.parse_args()

    # We don't necessarily want to send the `command` argument to the `run` method of the command.
    command_name = (
        parsed_arguments.command if parsed_arguments.command is not None else "help"
    )
    del parsed_arguments.command

    try:
        command_manager.execute(command_name, parsed_arguments)
    except Exception as error:
        message = (
            str(error)
            if len(str(error)) > 0
            else f"Something went wrong, please check the logs for more info: {repr(error)}"
        )

        messages.error(message, error)

    sys.exit()
