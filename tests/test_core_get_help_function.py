from jackman.core import get_help, registered_commands


def test_get_help_returns_all_commands():
    help_values = get_help()
    assert 'amount' in help_values.keys()
    assert 'commands' in help_values.keys()
    assert 'jackman_version' in help_values.keys()
    assert len(help_values['commands']) == len(registered_commands)
    assert len(help_values['commands']) == help_values['amount']
    assert len(registered_commands) == help_values['amount']
    assert type(help_values['commands']) is list

    if help_values['amount'] > 0:
        assert type(help_values['commands'][0]) is tuple


def test_get_help_for_build():
    help_values = get_help('build')
    assert 'amount' in help_values.keys()
    assert 'commands' in help_values.keys()
    assert 'jackman_version' in help_values.keys()
    assert help_values['amount'] == 1
    assert len(help_values['commands']) == help_values['amount']
    assert type(help_values['commands']) is list
    assert type(help_values['commands'][0]) is tuple

    command, documentation = help_values['commands'][0]
    assert registered_commands[command].__doc__ == documentation


def test_get_help_for_dev():
    help_values = get_help('dev')
    assert 'amount' in help_values.keys()
    assert 'commands' in help_values.keys()
    assert 'jackman_version' in help_values.keys()
    assert help_values['amount'] == 1
    assert len(help_values['commands']) == help_values['amount']
    assert type(help_values['commands']) is list
    assert type(help_values['commands'][0]) is tuple

    command, documentation = help_values['commands'][0]
    assert registered_commands[command].__doc__ == documentation


def test_get_help_for_create():
    help_values = get_help('create')
    assert 'amount' in help_values.keys()
    assert 'commands' in help_values.keys()
    assert 'jackman_version' in help_values.keys()
    assert help_values['amount'] == 1
    assert len(help_values['commands']) == help_values['amount']
    assert type(help_values['commands']) is list
    assert type(help_values['commands'][0]) is tuple

    command, documentation = help_values['commands'][0]
    assert registered_commands[command].__doc__ == documentation


def test_get_help_for_deploy():
    help_values = get_help('deploy')
    assert 'amount' in help_values.keys()
    assert 'commands' in help_values.keys()
    assert 'jackman_version' in help_values.keys()
    assert help_values['amount'] == 1
    assert len(help_values['commands']) == help_values['amount']
    assert type(help_values['commands']) is list
    assert type(help_values['commands'][0]) is tuple

    command, documentation = help_values['commands'][0]
    assert registered_commands[command].__doc__ == documentation