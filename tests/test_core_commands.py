import pytest

from sys import argv

from jackman.core import main, execute, show_help
from jackman.errors import CoreUnknownCommandError, CoreUnspecifiedCommandError


def test_mock_empty_call_to_main():
    assert main(['filename']) == show_help()


def test_actual_empty_call_to_main():
    with pytest.raises(CoreUnknownCommandError):
        assert main() == execute(argv)


def test_execute_with_error_command():
    argument_vector = ['core.py', '']
    with pytest.raises(CoreUnknownCommandError):
        execute(argument_vector)


def test_execute_with_too_few_arguments():
    argument_vector = ['core.py']
    with pytest.raises(CoreUnspecifiedCommandError):
        execute(argument_vector)


def test_execute_help():
    argument_vector = ['core.py', 'help']
    assert execute(argument_vector) == show_help()


def test_execute_help_from_main():
    argument_vector = ['core.py', 'help']
    assert main(argument_vector) == show_help()


def test_execute_deploy():
    pass
