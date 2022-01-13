from dataclasses import dataclass
from typing import ClassVar, Optional, Any

from colorama import Fore, Back, Style
from .logging import LogLevels


@dataclass
class MessageInterface:
    name: ClassVar[str]
    template: str = ''
    log_type: LogLevels = LogLevels.NOTSET

    def __str__(self) -> str:
        return self.template

    def as_formatted_string(self, msg: str, *args: Any, **kwargs: Any) -> Optional[str]:
        return self.template.format(*args, **kwargs, msg=msg, Fore=Fore, Back=Back, Style=Style)


@dataclass
class AskMessage(MessageInterface):
    name: ClassVar[str] = 'ask'
    template: str = '{Fore.YELLOW}> {msg}{Style.RESET_ALL}'

    def as_formatted_string(self, msg: str, *args: Any, **kwargs: Any) -> str:
        return input(self.template.format(msg=msg, Fore=Fore, Back=Back, Style=Style))


@dataclass
class DebugMessage(MessageInterface):
    name: ClassVar[str] = 'debug'
    template: str = ''
    log_type: LogLevels = LogLevels.DEBUG

    def as_formatted_string(self, msg: str, *args: Any, **kwargs: Any) -> None:
        return


@dataclass
class EchoMessage(MessageInterface):
    name: ClassVar[str] = 'echo'
    template: str = '{Fore.WHITE}{msg}{Style.RESET_ALL}'


@dataclass
class InfoMessage(MessageInterface):
    name: ClassVar[str] = 'info'
    header_template: str = '{Fore.BLUE}{msg}{Style.RESET_ALL}'
    template: str = '{Fore.WHITE}{msg}{Style.RESET_ALL}'
    log_type: LogLevels = LogLevels.INFO

    def as_formatted_string(self, msg: str, *args: Any, **kwargs: Any) -> str:
        if kwargs.get('header', False):
            return self.header_template.format(*args, **kwargs, msg=msg, Fore=Fore, Back=Back, Style=Style)
        else:
            return self.template.format(*args, **kwargs, msg=msg, Fore=Fore, Back=Back, Style=Style)


@dataclass
class WarnMessage(MessageInterface):
    name: ClassVar[str] = 'warn'
    template: str = '{Fore.YELLOW}{msg}{Style.RESET_ALL}'
    log_type: LogLevels = LogLevels.WARNING


@dataclass
class ErrorMessage(MessageInterface):
    name: ClassVar[str] = 'error'
    template: str = '{Fore.RED}{msg}{Style.RESET_ALL}'
    log_type: LogLevels = LogLevels.ERROR


@dataclass
class SuccessMessage(MessageInterface):
    name: ClassVar[str] = 'error'
    template: str = '{Fore.GREEN}{msg}{Style.RESET_ALL}'
    template_checkmark: str = '{Fore.GREEN}\u2713 {msg}{Style.RESET_ALL}'
    log_type: LogLevels = LogLevels.INFO

    def as_formatted_string(self, msg: str, *args: Any, **kwargs: Any) -> str:
        if kwargs.get('disable_checkmark', False):
            return self.template.format(*args, **kwargs, msg=msg, Fore=Fore, Back=Back, Style=Style)
        else:
            return self.template_checkmark.format(*args, **kwargs, msg=msg, Fore=Fore, Back=Back, Style=Style)
