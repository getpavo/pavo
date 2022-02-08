from typing import Optional
import sys

from pkg_resources import get_distribution

from pavo.utils import files, config
from pavo.builtins import Build, Create, Dev, Help
from pavo.core import CommandManager, PluginManager, messages


class PavoApp:
    def __init__(self) -> None:
        self.version = get_distribution('pavo').version
        self.plugin_manager = PluginManager()
        self.command_manager = CommandManager()
        self.command_manager.register(Build())
        self.command_manager.register(Create())
        self.command_manager.register(Dev())
        self.command_manager.register(Help(command_manager=self.command_manager))

    def discover_plugins(self) -> None:
        pass

    def run(self, args: Optional[list] = None) -> None:
        if not self.has_correct_version():
            messages.warning('Your Pavo config file version does not match your Pavo version.')

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

            messages.error(message, err)

        sys.exit()

    def has_correct_version(self) -> bool:
        if not files.cd_is_project():
            return True

        if config.get_config_value('version') == self.version:
            return True

        return False


def main() -> None:
    app = PavoApp()
    app.run(sys.argv[1:])


if __name__ == '__main__':
    main()
