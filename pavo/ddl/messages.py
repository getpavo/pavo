from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import ClassVar, Optional, Any, Type

from colorama import Fore, Back, Style
from .log import LogLevels


@dataclass
class MessageInterface:
    """MessageInterface, defining what data needs to be set for a custom message type."""
    name: ClassVar[str]
    template: str = ''
    log_level: LogLevels = LogLevels.NOTSET

    def __str__(self) -> str:
        return self.template

    def as_formatted_string(self, msg: str, *args: Any, **kwargs: Any) -> Optional[str]:
        """Formats the template with the provided message.

        Args:
            msg (str): The message that should be added to the template
            *args: Optional arguments to be added to the template.
            **kwargs: Optional keyword arguments to be added to the template.

        Returns:
            str: The formatted string.
        """
        return self.template.format(*args, **kwargs, msg=msg, Fore=Fore, Back=Back, Style=Style)

    def print(self, msg: str, *args: Any, **kwargs: Any) -> None:
        print(self.as_formatted_string(msg, *args, **kwargs))


class MessageHandlerInterface(ABC):
    @abstractmethod
    def print(self, message_type: str, msg: str, **kwargs: Any) -> bool:
        ...

    @abstractmethod
    def register(self, message_interface: Type[MessageInterface]) -> bool:
        ...


@dataclass
class AskMessage(MessageInterface):
    """Requests input from the user and returns it."""
    name: ClassVar[str] = 'ask'
    template: str = '{Fore.YELLOW}> {msg}{Style.RESET_ALL}'

    def as_formatted_string(self, msg: str, *args: Any, **kwargs: Any) -> str:
        return input(self.template.format(msg=msg, Fore=Fore, Back=Back, Style=Style))


@dataclass
class DebugMessage(MessageInterface):
    """Debug message that is sent to the logs, without showing in stdout."""
    name: ClassVar[str] = 'debug'
    template: str = ''
    log_level: LogLevels = LogLevels.DEBUG

    def as_formatted_string(self, msg: str, *args: Any, **kwargs: Any) -> None:
        return


@dataclass
class EchoMessage(MessageInterface):
    """Message that only shows in stdout, but not in the logs."""
    name: ClassVar[str] = 'echo'
    template: str = '{Fore.WHITE}{msg}{Style.RESET_ALL}'


@dataclass
class InfoMessage(MessageInterface):
    """Info message, can either be a header or a regular info message."""
    name: ClassVar[str] = 'info'
    header_template: str = '{Fore.BLUE}{msg}{Style.RESET_ALL}'
    template: str = '{Fore.WHITE}{msg}{Style.RESET_ALL}'
    log_level: LogLevels = LogLevels.INFO

    def as_formatted_string(self, msg: str, *args: Any, **kwargs: Any) -> str:
        if kwargs.get('header', False):
            return self.header_template.format(*args, **kwargs, msg=msg, Fore=Fore, Back=Back, Style=Style)

        return self.template.format(*args, **kwargs, msg=msg, Fore=Fore, Back=Back, Style=Style)


@dataclass
class WarnMessage(MessageInterface):
    """Warning message, for when something is prone to go wrong or needs attention."""
    name: ClassVar[str] = 'warn'
    template: str = '{Fore.YELLOW}{msg}{Style.RESET_ALL}'
    log_level: LogLevels = LogLevels.WARNING


@dataclass
class ErrorMessage(MessageInterface):
    """An error occurred, no fun here."""
    name: ClassVar[str] = 'error'
    template: str = '{Fore.RED}{msg}{Style.RESET_ALL}'
    log_level: LogLevels = LogLevels.ERROR


@dataclass
class SuccessMessage(MessageInterface):
    """Custom message to use on successful actions. Can be toggled between checkmark and regular green."""
    name: ClassVar[str] = 'success'
    template: str = '{Fore.GREEN}{msg}{Style.RESET_ALL}'
    template_checkmark: str = '{Fore.GREEN}\u2713 {msg}{Style.RESET_ALL}'
    log_level: LogLevels = LogLevels.INFO

    def as_formatted_string(self, msg: str, *args: Any, **kwargs: Any) -> str:
        if kwargs.get('disable_checkmark', False):
            return self.template.format(*args, **kwargs, msg=msg, Fore=Fore, Back=Back, Style=Style)

        return self.template_checkmark.format(*args, **kwargs, msg=msg, Fore=Fore, Back=Back, Style=Style)
