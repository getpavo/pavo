import logging
from pkg_resources import iter_entry_points, get_distribution
from sys import argv

from core.helpers import setup_logging, cd_is_project
from core.errors import CoreUnspecifiedCommandError, CoreUnknownCommandError, CoreInvalidExecutionDirectoryError

# TODO: Port most of this logic to the CLI project

setup_logging()
log = logging.getLogger(__name__)
registered_commands = {}
for entry_point in iter_entry_points('jackman.commands'):
    if entry_point.name not in registered_commands.keys():
        try:
            registered_commands[entry_point.name] = entry_point.load()
            log.debug(f'Found and successfully added {entry_point.name}')
        except Exception as e:
            log.exception(e, exc_info=False)
    else:
        log.debug(f'{entry_point.name} was already loaded by another source.')


def main(arguments=None):
    """Executes a specified command from argument vector or shows help when no command specified.

    Args:
        arguments (list): A list of arguments, starting with the filename, followed by command and optional kwargs.

    Returns:
        None
    """
    if not arguments:
        arguments = argv[1:]

    log.debug('Successfully started Jackman.')
    execute(arguments)


def execute(argument_vector):
    """Executes the command from the argument vector.

        Args:
            argument_vector (list): The argument vector to use when executing.

        Raises:
            CoreUnspecifiedCommandError: The command is not specified in the ``argument_vector``.
            CoreUnknownCommandError: The specified command is not recognized as a registered command.
            CoreInvalidExecutionDirectoryError: The directory to execute in, is not a project and command is not create.
        """
    log.debug(f'Executing with vector {argument_vector}')
    try:
        command = argument_vector[0]
    except IndexError:
        raise CoreUnspecifiedCommandError

    optional_arguments = argument_vector[1:]

    try:
        executable_command = registered_commands[command]
        if not cd_is_project() and command not in ['create', 'help']:
            raise CoreInvalidExecutionDirectoryError
        else:
            if not optional_arguments:
                executable_command()
            else:
                executable_command(optional_arguments)
    except KeyError:
        raise CoreUnknownCommandError


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
            'jackman_version': get_distribution("jackman_core").version
        }

    else:
        if specified_command not in registered_commands:
            raise CoreUnknownCommandError
        else:
            return {
                'amount': 1,
                'commands': [(specified_command, registered_commands[specified_command].__doc__)],
                'jackman_version': get_distribution("jackman_core").version
            }
