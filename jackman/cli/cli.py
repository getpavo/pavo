from sys import argv
from pkg_resources import iter_entry_points, get_distribution

from tabulate import tabulate

from jackman.cli.messages import echo, info, warn, error
from jackman.cli.errors import UnknownCommandError, UnspecifiedCommandError, InvalidExecutionDirectoryError
from jackman.core.helpers import cd_is_project


def main(args=None):
    if not args:
        args = argv[1:]

    try:
        command, optional_args = _parse(args)
        if optional_args is not None:
            command(*optional_args)
        else:
            command()
    except InvalidExecutionDirectoryError as e:
        error('You are executing Jackman in an invalid Jackman project. '
              'Please create a new project or navigate to a valid project directory.', e)
    except UnknownCommandError as e:
        error('The specified command could not be found, are you sure it is imported?', e)
    except UnspecifiedCommandError:
        warn('\nYou did not specify a Jackman command, so we are showing you some help.')
        _help()


def _get_commands():
    commands = {}

    for entry_point in iter_entry_points('jackman_commands'):
        if entry_point.name in commands:
            warn(f'Could not load {entry_point.name} again, because it has been defined already.')
        else:
            commands[entry_point.name] = entry_point.load()

    return commands


def _parse(args):
    """Parses arguments and throws an error when parsing to a command is not possible.

    Args:
        args (list): A list of arguments, starting with the command.

    Raises:
        UnspecifiedCommandError: No command was specified
        InvalidExecutionDirectoryError: The current directory is not a Jackman project.
        UnknownCommandError: The

    Returns:
        (function, list): The function and optional arguments that are to be executed.
    """
    if len(args) < 1:
        raise UnspecifiedCommandError

    selected = args[0]
    optional_args = args[1:]

    if not cd_is_project() and selected not in ['create', 'help']:
        raise InvalidExecutionDirectoryError

    available_commands = _get_commands()
    if selected not in available_commands or not callable(available_commands[selected]):
        raise UnknownCommandError

    return available_commands[selected], optional_args


def _help(specified_command=None):
    """Returns the help information for Jackman or a specific command.

    Args:
        specified_command (str): The command to show help for. Defaults to None.

    Raises:
        CoreUnknownCommandError: The specified command has not been registered or is unknown.
    """
    command_list = _get_commands()

    if not specified_command:
        table = []
        for command in command_list:
            try:
                table.append([command, command_list[command].__doc__.splitlines()[0]])
            except AttributeError:
                table.append([command, ''])

        info(f'\nShowing help for all {len(command_list)} Jackman commands:\n')
        echo(tabulate(table, tablefmt='plain'))

    else:
        if specified_command in command_list:
            info(f'\nShowing help for {specified_command}:\n')
            echo(command_list[specified_command].__doc__)
        else:
            raise CoreUnknownCommandError

    info(f'\nJackman v{get_distribution("jackman").version}\n')


if __name__ == '__main__':
    main(argv[1:])