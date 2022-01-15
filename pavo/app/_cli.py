from typing import Optional, Any, Tuple, Callable
import sys

from pkg_resources import get_distribution, WorkingSet, DistributionNotFound
from tabulate import tabulate

from pavo.ddl.commands import InjectedMethods
from pavo.utils import files, config, decorators
from pavo.core import HookManager, MessageHandler, CommandManager
from pavo.core.exceptions import UnknownCommandError, InvalidExecutionDirectoryError


class PavoApp:
    def __init__(self) -> None:
        self.version = get_distribution('pavo').version
        self.message_handler = MessageHandler()
        self.hook_manager = HookManager()

        injectables = InjectedMethods(
            msg_handler=self.message_handler,
            hook_manager=self.hook_manager
        )

        self.command_manager = CommandManager(injectables)

    def run(self, args: Optional[list] = None) -> None:
        self._check_version()

        try:
            if args is None or len(args) < 1:
                self.command_manager.execute('help')
            else:
                command = args[0]
                optional = args[1:]
                self.command_manager.execute(command, optional)
        except Exception as err:  # pylint: disable=broad-except
            if len(str(err)) > 0:
                message = str(err)
            else:
                message = f'Something went wrong, check the logs for more info: {repr(err)}'

            self.message_handler.print('error', message, exc=err)

        sys.exit()

    def _check_version(self) -> None:
        if files.cd_is_project() and config.get_config_value('version'):
            self.message_handler.print('warn', 'Your Pavo config file version does not match your Pavo version.')

    def show_help(self, specified_command: Optional[str] = None) -> None:
        if specified_command is None:
            table = []
            command_list = self.command_manager.registered_commands
            for (name, command) in command_list.items():
                table.append([name, command.help])

            self.message_handler.print('info', f'\nShowing help for all {len(command_list)} Pavo commands:\n')
            self.message_handler.print('echo', tabulate(table, tablefmt='plain'))
        else:
            if specified_command in self.command_manager.registered_commands:
                self.message_handler.print('info', f'\nShowing help for {specified_command}:\n')
                self.message_handler.print('echo', self.command_manager.registered_commands[specified_command].help)
            else:
                raise UnknownCommandError


def _main() -> None:
    app = PavoApp()
    app.run(sys.argv[1:])


if __name__ == '__main__':
    _main()
