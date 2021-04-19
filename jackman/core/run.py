from pkg_resources import iter_entry_points, get_distribution
from sys import argv

from jackman.core.helpers import cd_is_project
from jackman.core.errors import CoreUnspecifiedCommandError, CoreUnknownCommandError, CoreInvalidExecutionDirectoryError

from jackman.builtins.messages import debug, error, info, echo, warn


def main(arguments=None):
    """Executes a specified command from argument vector or shows help when no command specified.

    Args:
        arguments (list): A list of arguments, starting with the filename, followed by command and optional kwargs.

    Returns:
        None
    """
    registered_commands = {}
    for entry_point in iter_entry_points('jackman.commands'):
        if entry_point.name not in registered_commands.keys():
            try:
                registered_commands[entry_point.name] = entry_point.load()
                debug(f'Found and successfully added {entry_point.name}')
            except Exception as e:
                error(e, 'Something went wrong in the core Jackman process.', silent=True)
        else:
            debug(f'{entry_point.name} was already loaded by another source.')

    if not arguments:
        arguments = argv[1:]

    info('Successfully started Jackman.')
    execute(arguments)

def get_help(specified_command=None):
    """Returns the help information for Jackman or a specific command.

    Args:
        specified_command (str): The command to show help for. Defaults to None.

    Raises:
        CoreUnknownCommandError: The specified command has not been registered or is unknown.

    Returns:
        dict: A dictionary with the amount of commands, tuples with command and documentation and the version of jackman
    """
    if not specified_command:
        command_list = []
        for command in registered_commands:
            try:
                command_list.append((command, registered_commands[command].__doc__.splitlines()[0]))
            except AttributeError:
                command_list.append((command, ''))

        return {
            'amount': len(command_list),
            'commands': command_list,
            'jackman_version': get_distribution("jackman").version
        }

    else:
        if specified_command not in registered_commands:
            raise CoreUnknownCommandError
        else:
            return {
                'amount': 1,
                'commands': [(specified_command, registered_commands[specified_command].__doc__)],
                'jackman_version': get_distribution("jackman").version
            }


if __name__ == '__main__':
    main()
