import pytest
import logging
from colorama import init, Fore, Style

from jackman._cli.messages import ask, echo, info, warn, error, debug

# Initialize Colorama
init()


def test_ask_has_console_output(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '42')
    assert ask('What is the answer to life, the universe and everything?') == \
           input('What is the answer to life, the universe and everything?')


def test_ask_has_no_logs(caplog, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '42')
    ask('What is the answer to life, the universe and everything?')
    caplog.set_level(logging.DEBUG)
    assert caplog.records == []


def test_echo_has_console_output(capsys):
    echo('The answer to life')
    captured = capsys.readouterr()
    assert captured.out == f'{Fore.WHITE}The answer to life{Style.RESET_ALL}\n'


def test_echo_has_no_logs(caplog):
    echo('The answer to life')
    caplog.set_level(logging.DEBUG)
    assert caplog.records == []


def test_info_has_console_output(capsys):
    info('The answer to life')
    captured = capsys.readouterr()
    assert captured.out == f'{Fore.BLUE}The answer to life{Style.RESET_ALL}\n'


def test_info_has_no_logs(caplog):
    info('The answer to life')
    caplog.set_level(logging.DEBUG)
    assert caplog.records == []


def test_warn_console(capsys):
    warn('The answer to life')
    captured = capsys.readouterr()
    assert captured.out == f'{Fore.YELLOW}The answer to life{Style.RESET_ALL}\n'


def test_warn_has_logs(caplog):
    warn('The answer to life')
    assert len(caplog.records) > 0
    for record in caplog.records:
        assert record.levelname == 'WARNING'


def test_warn_logs_can_be_silenced(caplog):
    warn('The answer to life', disable_logging=True)
    assert caplog.records == []


def test_warn_logs_can_use_alt_logger(caplog):
    warn('The answer to life', logger_name='alternative')
    assert len(caplog.records) > 0
    for record in caplog.records:
        assert record.name == 'alternative'
        assert record.name != 'default'


def test_error_without_e_has_console_output(capsys):
    with pytest.raises(SystemExit):
        error('The answer to life')
    captured = capsys.readouterr()
    assert captured.out == f'{Fore.RED}The answer to life{Style.RESET_ALL}\n'


def test_error_without_e_has_no_logs(caplog):
    with pytest.raises(SystemExit):
        error('The answer to life')
    assert caplog.records == []


def test_error_with_e_has_console_output(capsys):
    try:
        raise Exception
    except Exception as e:
        with pytest.raises(SystemExit):
            error('The answer to life', e)

    captured = capsys.readouterr()
    assert captured.out == f'{Fore.RED}The answer to life{Style.RESET_ALL}\n'


def test_error_with_e_has_logs(caplog):
    try:
        raise Exception
    except Exception as e:
        with pytest.raises(SystemExit):
            error('The answer to life', e)

    assert len(caplog.records) > 0
    for record in caplog.records:
        assert record.levelname == 'ERROR'


def test_error_logs_can_use_alt_logger(caplog):
    try:
        raise Exception
    except Exception as e:
        with pytest.raises(SystemExit):
            error('The answer to life', e, logger_name='alternative')

    assert len(caplog.records) > 0
    for record in caplog.records:
        assert record.levelname == 'ERROR'
        assert record.name == 'alternative'
        assert record.name != 'default'


def test_error_logs_can_be_silenced(caplog):
    try:
        raise Exception
    except Exception as e:
        with pytest.raises(SystemExit):
            error('The answer to life', e, disable_logging=True)

    assert caplog.records == []


def test_debug_has_no_console_output(capsys):
    debug('The answer to life')
    captured = capsys.readouterr()
    assert captured.out == ''


def test_debug_has_logs(caplog):
    caplog.set_level(logging.DEBUG)
    debug('The answer to life')
    assert len(caplog.records) > 0
    for record in caplog.records:
        assert record.levelname == 'DEBUG'


def test_debug_logs_can_use_alt_logger(caplog):
    caplog.set_level(logging.DEBUG)
    debug('The answer to life', logger_name='alternative')
    assert len(caplog.records) > 0
    for record in caplog.records:
        assert record.name == 'alternative'
        assert record.name != 'default'


def test_debug_logs_cannot_be_silenced(caplog):
    caplog.set_level(logging.DEBUG)
    debug('The answer to life', disable_logging=True)
    assert len(caplog.records) > 0
