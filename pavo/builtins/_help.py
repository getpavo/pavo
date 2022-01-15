from dataclasses import dataclass
from typing import Optional

from pavo.ddl.commands import CommandInterface
from pavo.core.exceptions import UnknownCommandError


@dataclass
class Help(CommandInterface):
    name: str = 'help'
    help: str = 'Shows this help prompt.'
    allow_outside_project: bool = True

    def run(self, args: Optional[list] = None) -> None:
        if args is not None and len(args) > 1:
            raise UnknownCommandError

        print('Here is the help prompt boys')
