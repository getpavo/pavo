import argparse
from typing import Any
from dataclasses import dataclass

from pavo.ddl.commands import CommandInterface, CommandManagerInterface
from pavo.core.exceptions import UnknownCommandError, InvalidExecutionDirectoryError
from pavo.utils import files


@dataclass
class CommandManager(CommandManagerInterface):
    """Manages the registered commands, and executes commands when requested."""

    def register(self, command: CommandInterface) -> bool:
        """Register a command to the command manager.

        Args:
            command: The command object to register.

        Returns:
            bool: Whether the registration succeeded.
        """
        if command.name.lower() in self.registered_commands:
            raise NotImplementedError

        self.registered_commands[command.name.lower()] = command
        return True

    def execute(self, command_name: str, args: argparse.Namespace) -> None:
        """Executes a command, based on the string name.

        Args:
            command_name: The name of the command to execute.
            *args: Optional arguments you want to provide to the executed command.
        """
        if command_name not in self.registered_commands:
            raise UnknownCommandError

        command = self.registered_commands[command_name]

        if command.allow_outside_project is False and not files.cd_is_project():
            raise InvalidExecutionDirectoryError

        command.run(args)
