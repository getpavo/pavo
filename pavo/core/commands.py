from typing import Type, Any
from dataclasses import dataclass

from pavo.ddl.commands import CommandInterface, CommandManagerInterface, InjectedMethods
from pavo.builtins import Build, Create, Dev, Help
from pavo.core.exceptions import UnknownCommandError, InvalidExecutionDirectoryError
from pavo.utils import files


@dataclass
class CommandManager(CommandManagerInterface):
    def __post_init__(self) -> None:
        self.registered_commands: dict[str, CommandInterface] = {}
        self.register(Build)
        self.register(Create)
        self.register(Dev)
        self.register(Help)

    def register(self, command: Type[CommandInterface]) -> bool:
        if command.name.lower() in self.registered_commands:
            raise NotImplementedError

        try:
            self.registered_commands[command.name.lower()] = command(injected=self.injectables)
        except ValueError:
            return False

        return True

    def execute(self, command_name: str, *args: Any) -> None:
        if command_name not in self.registered_commands:
            raise UnknownCommandError

        command = self.registered_commands[command_name]

        if command.allow_outside_project is False and not files.cd_is_project():
            raise InvalidExecutionDirectoryError

        command.run(*args)
