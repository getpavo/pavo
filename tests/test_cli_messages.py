import pytest
import logging
from colorama import init, Fore, Style

from jackman.cli.messages import ask, echo, info, warn, error, debug

# Initialize Colorama
init()


def test_ask(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '42')
    assert ask('What is the answer to life, the universe and everything?') == \
           input('What is the answer to life, the universe and everything?')


def test_ask_logs(caplog, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '42')
    ask('What is the answer to life, the universe and everything?')
    caplog.set_level(logging.DEBUG)
    assert caplog.records == []


def test_echo_console(capsys):
    echo('The answer to life')
    captured = capsys.readouterr()
    assert captured.out == f'{Fore.WHITE}The answer to life{Style.RESET_ALL}\n'


def test_echo_logs(caplog):
    echo('The answer to life')
    caplog.set_level(logging.DEBUG)
    assert caplog.records == []


def test_info_console(capsys):
    info('The answer to life')
    captured = capsys.readouterr()
    assert captured.out == f'{Fore.BLUE}The answer to life{Style.RESET_ALL}\n'


def test_warn_console(capsys):
    warn('The answer to life')
    captured = capsys.readouterr()
    assert captured.out == f'{Fore.YELLOW}The answer to life{Style.RESET_ALL}\n'


def test_error_without_e_console(capsys):
    with pytest.raises(SystemExit):
        error('The answer to life')
    captured = capsys.readouterr()
    assert captured.out == f'{Fore.RED}The answer to life{Style.RESET_ALL}\n'


def test_debug_console(capsys):
    debug('The answer to life')
    captured = capsys.readouterr()
    assert captured.out == ''
