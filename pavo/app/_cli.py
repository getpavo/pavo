from typing import Optional
import sys

from pkg_resources import get_distribution

from pavo.utils import files, config
from pavo.builtins import Build, Create, Dev, Help
from pavo.core import MessageHandler, CommandManager, PluginManager


class PavoApp:
    def __init__(self) -> None:
        self.version = get_distribution('pavo').version
        self.message_handler = MessageHandler()
        self.plugin_manager = PluginManager()
        self.command_manager = CommandManager()
        self.command_manager.register(Build(msg_handler=self.message_handler))
        self.command_manager.register(Create())
        self.command_manager.register(Dev(msg_handler=self.message_handler))
        self.command_manager.register(Help(command_manager=self.command_manager, msg_handler=self.message_handler))

    def discover_plugins(self) -> None:
        pass

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


def main() -> None:
    app = PavoApp()
    app.run(sys.argv[1:])


if __name__ == '__main__':
    main()
