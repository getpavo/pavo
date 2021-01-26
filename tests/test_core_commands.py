import pytest

from jackman.core import main, execute, show_help
from jackman.errors import CoreUnknownCommandError


def test_empty_call_to_main():
    assert main(['filename']) == show_help()


def test_execute_with_error_command():
    argument_vector = ['core.py', '']
    with pytest.raises(CoreUnknownCommandError):
        execute(argument_vector)


def test_execute_build():
    pass


def test_execute_dev():
    pass


def test_execute_command_outside_jackman_project():
    pass


def test_execute_create_inside_jackman_project():
    pass


def test_execute_create_outside_jackman_project():
    pass


def test_execute_help():
    argument_vector = ['core.py', 'help']
    assert execute(argument_vector) == show_help()


def test_execute_deploy():
    pass
