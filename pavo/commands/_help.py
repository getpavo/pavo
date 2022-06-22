from dataclasses import dataclass
from typing import Optional
import argparse

import tabulate

from pavo.utils import version
from pavo.ddl.commands import CommandInterface, CommandManagerInterface
from pavo.core.exceptions import UnknownCommandError
from pavo.core import messages


@dataclass(kw_only=True)
class Help(CommandInterface):
    """Built-in 'help' command."""

    command_manager: CommandManagerInterface
    name: str = "help"
    help: str = "Shows this help prompt."
    allow_outside_project: bool = True

    def run(self, args: argparse.Namespace) -> None:
        """Shows help prompt for all commands or a single command, if specified.

        Args:
            args: The arguments provided by the caller.
        """
        if args.command is None:
            table = []
            command_list = self.command_manager.registered_commands
            for (name, command) in command_list.items():
                table.append([name, command.help])

            messages.info(
                f"\nShowing help for all {len(command_list)} Pavo commands:\n"
            )
            messages.echo(tabulate.tabulate(table, tablefmt="plain"))
            messages.info(f'\nPavo v{pkg_resources.get_distribution("pavo").version}')
            return

        if args.command not in self.command_manager.registered_commands:
            raise UnknownCommandError(
                "Could not find help for the specified command. Are you sure it exists?"
            )

        doc_string = self.command_manager.registered_commands[args.command].run.__doc__
        if doc_string is None:
            doc_string = self.command_manager.registered_commands[args.command].help

        messages.info(f"\nShowing help for {args.command}:\n")
        messages.echo(doc_string)
        messages.info(f"\nPavo v{version.DISTRIBUTION_VERSION}")

    def setup_parser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--command",
            default=None,
            help="The command you wish to see the help text for, leave blank for an overview of all commands.",
        )
