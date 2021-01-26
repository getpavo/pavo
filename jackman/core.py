import logging
from pkg_resources import iter_entry_points, get_distribution
from sys import argv
from tabulate import tabulate

from jackman.helpers import setup_logging, cd_is_project, get_cwd
from jackman.errors import CoreUnspecifiedCommandError, CoreUnknownCommandError, CoreInvalidExecutionDirectory, CoreHelpCommandTooLong


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
    """Main entry point. Executes the specified command or shows help when no command specified.

    Returns:
        None
    """
    if not arguments:
        arguments = argv

    log.debug('Successfully started Jackman.')
    if len(arguments) > 1:
        execute(arguments)
    else:
        show_help()


def execute(argument_vector):
    """Executes the command from the argument vector.

        Args:
            argument_vector (list): The argument vector to use when executing.

        Raises:
            CoreUnspecifiedCommandError: The command is not specified in the ``argument_vector``.
            CoreUnknownCommandError: The specified command is not recognized as a registered command.
            CoreInvalidExecutionDirectory: The directory to execute in, is not a valid project and command is not create.
            CoreHelpCommandTooLong: The specified command is too long to show help for. Max: ``jackman help command``
        """
    log.debug(f'Executing with vector {argument_vector}')
    try:
        command = argument_vector[1]
    except IndexError:
        raise CoreUnspecifiedCommandError

    try:
        executable_command = registered_commands[command]
        if not cd_is_project() and command not in ['create', 'help']:
            raise CoreInvalidExecutionDirectory
        else:
            executable_command()
    except KeyError:
        if command in ['help', '--help', '-h']:
            if len(argument_vector) == 3:
                show_help(argument_vector[2])
            elif len(argument_vector) > 3:
                raise CoreHelpCommandTooLong
            show_help()
        else:
            raise CoreUnknownCommandError


def show_help(specified_command=None):
    """Shows the help for the project or a specific command.

    Args:
        specified_command (str): The command to show help for. Defaults to None.

    Note:
        When no command is specified, we show general help for the Jackman project.

    Raises:
        CoreUnknownCommandError: The specified command has not been registered or is unknown.

    Returns:
        None
    """
    if not specified_command:
        command_list = []
        for command in registered_commands:
            try:
                command_list.append((command, registered_commands[command].__doc__.splitlines()[0]))
            except AttributeError:
                command_list.append((command, ''))

        # TODO: Reserve help as command
        if 'help' not in command_list:
            command_list.append(('help', 'Shows this information prompt'))

        print('')
        print(f'There are {len(command_list)} commands available.')
        print('')
        print(tabulate(command_list, tablefmt='plain'))
        print('')
        print('For specific information about a command, run "jackman help <command_name>"')
        print('')
        print(f'Jackman v{get_distribution("jackman").version}')
        print('')
    else:
        if specified_command not in registered_commands:
            raise CoreUnknownCommandError
        else:
            print('')
            print(f'Showing documentation for {specified_command}')
            print('')
            print(registered_commands[specified_command].__doc__)
