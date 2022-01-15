from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Optional, Any, Type

from pavo.ddl.messages import MessageHandlerInterface
from pavo.ddl.hooks import HookManagerInterface


@dataclass
class InjectedMethods:
    """Contains methods and classes that get injected in every command.

    Note:
        The InjectedMethods do not contain a command manager, because it is injected live.
    """
    msg_handler: MessageHandlerInterface
    hook_manager: HookManagerInterface


@dataclass  # type: ignore
class CommandInterface(ABC):
    injected: InjectedMethods
    name: str
    help: str
    allow_outside_project: bool = False

    @abstractmethod
    def run(self, args: Optional[list] = None) -> None:
        ...


@dataclass  # type: ignore
class CommandManagerInterface(ABC):
    passed_injectables: InjectedMethods

    @abstractmethod
    def register(self, command: CommandInterface) -> bool:
        ...

    @abstractmethod
    def execute(self, command_name: str, *args: Any) -> None:
        ...

    @property
    def injectables(self):
        self.passed_injectables.cmd_manager = self
        return self.passed_injectables

# For reasons why types are being ignored, see: https://github.com/python/mypy/issues/5374
