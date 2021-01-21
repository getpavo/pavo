import pytest
from jackman.core import execute, show_help
from jackman.build import main as build_main_function


def test_get_help_no_specified_command():
    argument_vector = ['core.py', 'help']
    assert execute(argument_vector) == show_help()


def test_get_help_specified_command_not_exists(caplog):
    argument_vector = ['core.py', 'help', '']
    execute(argument_vector)
    assert caplog.records
    for record in caplog.records:
        assert record.levelname == "ERROR"
        assert record.msg == f'The specified command {argument_vector[2]} is not recognized as a Jackman command.'


def test_get_help_specified_command_too_long(caplog):
    argument_vector = ['core.py', 'help', 'build', 'test']
    execute(argument_vector)
    assert caplog.records
    for record in caplog.records:
        assert record.levelname == "ERROR"
        assert record.msg == 'The specified command is too long. Please enter only one command: jackman help <command>'


def test_get_help_command_exists(capsys):
    argument_vector = ['core.py', 'help', 'build']
    execute(argument_vector)
    captured = capsys.readouterr()
    assert build_main_function.__doc__ in captured.out
