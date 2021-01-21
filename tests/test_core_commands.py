from jackman.core import main, execute, show_help


def test_empty_call_to_main():
    assert main() == show_help()


def test_execute_with_error_command(caplog):
    argument_vector = ['core.py', '']
    execute(argument_vector)

    assert caplog.records
    for record in caplog.records:
        assert record.levelname == "CRITICAL"
        assert 'Could not execute.' in record.msg
        assert '"" is not recognized as a valid Jackman command' in record.msg


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
