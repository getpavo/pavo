from sys import argv
from pkg_resources import iter_entry_points, get_distribution

from tabulate import tabulate

from jackman.cli.messages import echo, info, warn, error
from jackman.core.errors import CoreUnknownCommandError, CoreUnspecifiedCommandError, CoreInvalidExecutionDirectoryError
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
    except Exception as e:
        # TODO: Add error handling here
        error(repr(e), e)


def _get_commands():
    commands = {}

    for entry_point in iter_entry_points('jackman_commands'):
        if entry_point.name in commands:
            warn(f'Could not load {entry_point.name} again, because it has been defined already.')
        else:
            commands[entry_point.name] = entry_point.load()

    return commands


def _parse(args):
    if len(args) < 1:
        raise CoreUnspecifiedCommandError

    selected = args[0]
    optional_args = args[1:]

    if not cd_is_project() and selected not in ['create', 'help']:
        raise CoreInvalidExecutionDirectoryError

    available_commands = _get_commands()
    if selected not in available_commands or not callable(available_commands[selected]):
        raise CoreUnknownCommandError

    return available_commands[selected], optional_args


def _help(specified_command=None):
    """Returns the help information for Jackman or a specific command.
    TODO: Add specific command support

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
