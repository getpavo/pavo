import pytest

from jackman.core import execute, show_help
from jackman.build import main as build_main_function
from jackman.errors import CoreHelpCommandTooLong, CoreUnknownCommandError


def test_get_help_no_specified_command():
    argument_vector = ['core.py', 'help']
    assert execute(argument_vector) == show_help()


def test_get_help_specified_command_not_exists():
    argument_vector = ['core.py', 'help', 'weoifjewioufhewiufhewiufhri']
    with pytest.raises(CoreUnknownCommandError):
        execute(argument_vector)


def test_get_help_specified_command_too_long():
    argument_vector = ['core.py', 'help', 'build', 'test']
    with pytest.raises(CoreHelpCommandTooLong):
        execute(argument_vector)


def test_get_help_command_exists(capsys):
    argument_vector = ['core.py', 'help', 'build']
    execute(argument_vector)
    captured = capsys.readouterr()
    assert build_main_function.__doc__ in captured.out
