import pytest

from jackman.core import main, execute
from jackman.errors import CoreUnknownCommandError, CoreUnspecifiedCommandError


def test_mock_empty_call_to_main():
    with pytest.raises(CoreUnspecifiedCommandError):
        main(['filename'])


def test_execute_with_error_command():
    argument_vector = ['core.py', '']
    with pytest.raises(CoreUnknownCommandError):
        execute(argument_vector)


def test_execute_with_too_few_arguments():
    argument_vector = ['core.py']
    with pytest.raises(CoreUnspecifiedCommandError):
        execute(argument_vector)


def test_execute_deploy():
    pass
