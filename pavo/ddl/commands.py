from dataclasses import dataclass, field
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
    registered_commands: dict[str, CommandInterface] = field(default_factory=dict)

    @abstractmethod
    def register(self, command: Type[CommandInterface]) -> bool:
        ...

    @abstractmethod
    def execute(self, command_name: str, *args: Any) -> None:
        ...

    @property
    def injectables(self) -> InjectedMethods:
        self.passed_injectables.cmd_manager = self  # type: ignore
        return self.passed_injectables

# For reasons why types of the dataclass are being ignored, see: https://github.com/python/mypy/issues/5374
# Type ignore is also used to silence a warning about the attribute not existing, because we add it dynamically.
