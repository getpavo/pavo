import pytest
from jackman.cli.messages import ask, echo, info, warn, error, debug


def test_ask(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '42')
    assert ask('What is the answer to life, the universe and everything?') == \
           input('What is the answer to life, the universe and everything?')


def test_echo_console(capsys):
    echo('The answer to life')
    captured = capsys.readouterr()
    assert captured.out == '\x1b[37mThe answer to life\x1b[0m\n'


def test_info_console(capsys):
    info('The answer to life')
    captured = capsys.readouterr()
    assert captured.out == '\x1b[34mThe answer to life\x1b[0m\n'


def test_warn_console(capsys):
    warn('The answer to life')
    captured = capsys.readouterr()
    assert captured.out == '\x1b[33mThe answer to life\x1b[0m\n'


def test_error_without_e_console(capsys):
    with pytest.raises(SystemExit):
        error('The answer to life')
    captured = capsys.readouterr()
    assert captured.out == '\x1b[31mThe answer to life\x1b[0m\n'


def test_debug_console(capsys):
    debug('The answer to life')
    captured = capsys.readouterr()
    assert captured.out == ''
