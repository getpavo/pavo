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
    # We need to set these shared options on the main parser, but also all subparsers.
    default_options = {
        "conflict_handler": "resolve",
        "allow_abbrev": False,
        "add_help": False,
        "exit_on_error": False,
    }

    argument_parser = argparse.ArgumentParser(**default_options)
    subparsers = argument_parser.add_subparsers()

    for command in commands:
        command_parser = subparsers.add_parser(command.name, **default_options)
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

    # Fetch the command from argument vector, so that it doesn't influence the parsed_arguments in any way.
    command = sys.argv[1] if len(sys.argv) > 1 else "help"

    try:
        command_manager.execute(command, parsed_arguments)
    except Exception as error:
        message = (
            str(error)
            if len(str(error)) > 0
            else f"Something went wrong, please check the logs for more info: {repr(error)}"
        )

        messages.error(message, error)

    sys.exit()
