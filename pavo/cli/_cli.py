from typing import Optional, Any, Tuple, Callable
import sys

from pkg_resources import get_distribution, WorkingSet, DistributionNotFound
from tabulate import tabulate

from pavo.helpers import files, config, decorators

from ._messager import handle_message
from ._errors import UnknownCommandError, UnspecifiedCommandError, InvalidExecutionDirectoryError


def _main(args: Optional[list] = None) -> None:
    """Main entry point for the CLI application.

    Args:
        args (list): List of arguments to be parsed and used, first one being the command.
    """
    if not args:
        args = sys.argv[1:]

    if files.cd_is_project() and config.get_config_value('version') != get_distribution("pavo").version:
        handle_message('warn', 'Your Pavo configuration file version does not match your Pavo version.')

    try:
        command, optional_args = _parse(args)
        if optional_args is not None:
            command(*optional_args)
        else:
            command()
    except UnspecifiedCommandError:
        handle_message('warn', '\nYou did not specify a Pavo command, so we are showing you some help.')
        _help()
    except Exception as err:  # pylint: disable=broad-except
        message = str(err) if len(str(err)) > 0 else f'Something went wrong, check the logs for more info: {repr(err)}'
        handle_message('error', message, exc=err)

    sys.exit()


def _get_commands() -> dict[str, Any]:
    """Get a list of all commands based on name in 'pavo_commands' namespace.

    This function finds installed modules and checks whether they are activated in the plugin section of the
    Pavo configuration file. If this is the case, the 'pavo' entry points will be loaded and made
    available to the CLI.

    Returns:
        dict: A dictionary of all commands mapped from name to function.
    """
    commands = {}

    # Create a WorkingSet with core Pavo functionality
    working_set = WorkingSet(entries=[])
    working_set.add(get_distribution('pavo'))

    # Get all activated plugins and try adding them to the working set
    try:
        activated_plugins = config.get_config_value('plugins')
        if isinstance(activated_plugins, list):
            for plugin in activated_plugins:
                try:
                    working_set.add(get_distribution(plugin))
                except DistributionNotFound:
                    handle_message('warn', f'Could not load commands from {plugin}. Are you sure it is installed?')
                except TypeError as err:
                    handle_message('err', 'Fatal error when trying to load commands. Please check your config file '
                                          'and the logs.', exc=err)
    except FileNotFoundError:
        # If outside a Pavo project use *all* installed packages to find Pavo commands.
        working_set = WorkingSet()

    # Iterate over all entry points in the working set
    for entry_point in working_set.iter_entry_points('pavo_commands'):
        if entry_point.name in commands:
            handle_message('warn', f'Could not load {entry_point.name} again, because it has been defined already.')
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
    if (not files.cd_is_project()
            and (not hasattr(func, 'allowed_outside_project') or func.allowed_outside_project is False)):
        raise InvalidExecutionDirectoryError

    return func, optional_args


@decorators.allow_outside_project
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
        for command in command_list:  # pylint: disable=consider-using-dict-items
            try:
                table.append([command, command_list[command].__doc__.splitlines()[0]])
            except AttributeError:
                table.append([command, ''])

        handle_message('info', f'\nShowing help for all {len(command_list)} Pavo commands:\n')
        handle_message('echo', tabulate(table, tablefmt='plain'))

    else:
        if specified_command in command_list:
            handle_message('info', f'\nShowing help for {specified_command}:\n')
            handle_message('echo', command_list[specified_command].__doc__)
        else:
            raise UnknownCommandError

    handle_message('info', f'\nPavo v{get_distribution("pavo").version}\n')
    sys.exit()


if __name__ == '__main__':
    _main(sys.argv[1:])
