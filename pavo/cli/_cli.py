from sys import argv
from pkg_resources import get_distribution, WorkingSet, DistributionNotFound
from typing import Optional, Any, Tuple, Callable

from tabulate import tabulate

from ._messages import echo, info, warn, error
from .errors import UnknownCommandError, UnspecifiedCommandError, InvalidExecutionDirectoryError

from pavo.cli import Broadcast
from pavo.helpers.files import cd_is_project
from pavo.helpers.config import get_config_value
from pavo.helpers.decorators import allow_outside_project


def _main(args: Optional[list] = None) -> None:
    """Main entry point for the CLI application.

    Args:
        args (list): List of arguments to be parsed and used, first one being the command.
    """
    if not args:
        args = argv[1:]

    if cd_is_project() and get_config_value('version') != get_distribution("pavo").version:
        warn('Your Pavo configuration file version does not match your Pavo version.')

    listener = Broadcast().subscribe()

    try:
        command, optional_args = _parse(args)
        listener.start()
        if optional_args is not None:
            command(*optional_args)
        else:
            command()
    except UnspecifiedCommandError:
        warn('\nYou did not specify a Pavo command, so we are showing you some help.')
        _help()
    except Exception as e:
        message = str(e) if len(str(e)) > 0 else f'Something went wrong, check the logs for more info: {repr(e)}'
        error(message, e)
        # TODO: Remove tmp folders when they are not used to serve a website locally

    # Wait for all messages to be listened to by the listener daemon
    while Broadcast().spy():
        pass

    exit()


def _get_commands() -> dict[str, Any]:
    """Get a list of all commands based on name in 'pavo_commands' namespace.

    This function finds installed modules and checks whether or not they are activated in the plugins section of the
    Pavo configuration file. If this is the case, the 'pavo' entry points will be loaded and made
    available to the CLI.

    Returns:
        dict: A dictionary of all commands mapped from name to function.
    """
    commands = {}

    # Create a WorkingSet with core Pavo functionality
    ws = WorkingSet(entries=[])
    ws.add(get_distribution('pavo'))

    # Get all activated plugins and try adding them to the working set
    try:
        activated_plugins = get_config_value('plugins')
        if isinstance(activated_plugins, list):
            for plugin in activated_plugins:
                try:
                    ws.add(get_distribution(plugin))
                except DistributionNotFound:
                    warn(f'Could not load commands from {plugin}. Are you sure the module is installed?')
                except TypeError as e:
                    error(f'Fatal error when trying to load commands. Please check your config file and the logs.', e)
    except FileNotFoundError:
        # If outside of a Pavo project use *all* installed packages to find Pavo commands.
        ws = WorkingSet()

    # Iterate over all entry points in the working set
    for entry_point in ws.iter_entry_points('pavo_commands'):
        if entry_point.name in commands:
            warn(f'Could not load {entry_point.name} again, because it has been defined already.')
        else:
            commands[entry_point.name] = entry_point.load()

    return commands


def _parse(args: list[str]) -> Tuple[Callable, list[str]]:
    """Parses arguments and throws an error when parsing to a command is not possible.

    Args:
        args (list): A list of arguments, starting with the command.

    Returns:
        (function, list): The function and optional arguments that are to be executed.

    Raises:
        UnspecifiedCommandError: No command was specified
        InvalidExecutionDirectoryError: The current directory is not a Pavo project.
        UnknownCommandError: The specified command has not been registered or is unknown.
    """
    if len(args) < 1:
        raise UnspecifiedCommandError

    selected = args[0]
    optional_args = args[1:]

    available_commands = _get_commands()

    if selected not in available_commands:
        raise UnknownCommandError

    func = available_commands[selected]
    if not cd_is_project() and (not hasattr(func, 'allowed_outside_project') or func.allowed_outside_project is False):
        raise InvalidExecutionDirectoryError

    return func, optional_args


@allow_outside_project
def _help(specified_command: str = None) -> None:
    """Prints the help information for Pavo or a specific command.

    Args:
        specified_command (str): The command to show help for. Defaults to None.

    Raises:
        UnknownCommandError: The specified command has not been registered or is unknown.
    """
    command_list = _get_commands()

    if not specified_command:
        table = []
        for command in command_list:
            try:
                table.append([command, command_list[command].__doc__.splitlines()[0]])
            except AttributeError:
                table.append([command, ''])

        info(f'\nShowing help for all {len(command_list)} Pavo commands:\n')
        echo(tabulate(table, tablefmt='plain'))

    else:
        if specified_command in command_list:
            info(f'\nShowing help for {specified_command}:\n')
            echo(command_list[specified_command].__doc__)
        else:
            raise UnknownCommandError

    info(f'\nPavo v{get_distribution("pavo").version}\n')
    exit()


if __name__ == '__main__':
    _main(argv[1:])
