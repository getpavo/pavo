from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Optional, Any, Type

from pavo.ddl.messages import MessageHandlerInterface
from pavo.ddl.plugins import PluginManagerInterface


@dataclass(kw_only=True)  # type: ignore
class CommandInterface(ABC):
    name: str
    help: str
    allow_outside_project: bool

    @abstractmethod
    def run(self, args: Optional[list] = None) -> None:
        ...


@dataclass  # type: ignore
class CommandManagerInterface(ABC):
    registered_commands: dict[str, CommandInterface] = field(default_factory=dict)

    @abstractmethod
    def register(self, command: CommandInterface) -> bool:
        ...

    @abstractmethod
    def execute(self, command_name: str, *args: Any) -> None:
        ...

    def help(self):
        pass

# For reasons why types of the dataclass are being ignored, see: https://github.com/python/mypy/issues/5374
