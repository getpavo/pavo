from dataclasses import dataclass
from typing import Optional
import pkg_resources

import tabulate

from pavo.ddl.commands import CommandInterface, CommandManagerInterface
from pavo.core.exceptions import UnknownCommandError
from pavo.core import messages


@dataclass(kw_only=True)
class Help(CommandInterface):
    """Built-in 'help' command."""
    command_manager: CommandManagerInterface
    name: str = 'help'
    help: str = 'Shows this help prompt.'
    allow_outside_project: bool = True

    def run(self, args: Optional[list] = None) -> None:
        """Shows help prompt for all commands or a single command, if specified.

        Args:
            args: The arguments provided by the caller.
        """
        if args is None or len(args) == 0:
            table = []
            command_list = self.command_manager.registered_commands
            for (name, command) in command_list.items():
                table.append([name, command.help])

            messages.info(f'\nShowing help for all {len(command_list)} Pavo commands:\n')
            messages.echo(tabulate.tabulate(table, tablefmt='plain'))
        else:
            if len(args) > 1 or args[0] not in self.command_manager.registered_commands:
                raise UnknownCommandError("Could not find help for the specified command. Are you sure it exists?")
            if args[0] in self.command_manager.registered_commands:
                doc_string = self.command_manager.registered_commands[args[0]].run.__doc__
                if doc_string is None:
                    doc_string = self.command_manager.registered_commands[args[0]].help

                messages.info(f'\nShowing help for {args[0]}:\n')
                messages.echo(doc_string)
            else:
                raise UnknownCommandError("Could not find help for the specified command. Are you sure it exists?")

        messages.info(f'\nPavo v{pkg_resources.get_distribution("pavo").version}')
