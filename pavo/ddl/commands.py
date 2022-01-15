from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Optional, Any, Type

from pavo.ddl.messages import MessageHandlerInterface


@dataclass  # type: ignore
class CommandInterface(ABC):
    injected_message_handler: MessageHandlerInterface
    name: str = ''
    help: str = ''
    allow_outside_project: bool = False

    @abstractmethod
    def run(self, args: Optional[list] = None) -> None:
        ...


@dataclass  # type: ignore
class CommandManagerInterface(ABC):
    injected_message_handler: MessageHandlerInterface

    @abstractmethod
    def register(self, command: CommandInterface) -> bool:
        ...

    @abstractmethod
    def execute(self, command_name: str, *args: Any) -> None:
        ...


# For reasons why types are being ignored, see: https://github.com/python/mypy/issues/5374
