from typing import Any
from dataclasses import dataclass

from pavo.ddl.commands import CommandInterface, CommandManagerInterface
from pavo.core.exceptions import UnknownCommandError, InvalidExecutionDirectoryError
from pavo.utils import files


@dataclass
class CommandManager(CommandManagerInterface):
    def register(self, command: CommandInterface) -> bool:
        if command.name.lower() in self.registered_commands:
            raise NotImplementedError

        self.registered_commands[command.name.lower()] = command
        return True

    def execute(self, command_name: str, *args: Any) -> None:
        if command_name not in self.registered_commands:
            raise UnknownCommandError

        command = self.registered_commands[command_name]

        if command.allow_outside_project is False and not files.cd_is_project():
            raise InvalidExecutionDirectoryError

        command.run(*args)
