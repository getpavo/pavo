import logging

from colorama import init, Fore, Style
from threading import Thread

from jackman.cli import Broadcast, broadcast_message

# Initialize Colorama
init()


def test_broadcast_init_works_correctly():
    broadcast = Broadcast()
    assert broadcast._unheard_messages == []
    assert 'echo' in broadcast._broadcast_types
    assert 'info' in broadcast._broadcast_types
    assert 'debug' in broadcast._broadcast_types
    assert 'warn' in broadcast._broadcast_types
    assert 'error' in broadcast._broadcast_types


def test_broadcast_message_invalid_type():
    assert broadcast_message('invalid', 'test') is False


def test_broadcast_message_valid_type():
    assert broadcast_message('echo', 'The answer to life.') is True
    assert broadcast_message('info', 'The answer to life.') is True
    assert broadcast_message('debug', 'The answer to life.') is True
    assert broadcast_message('warn', 'The answer to life.') is True
    assert broadcast_message('error', 'The answer to life.') is True


def test_broadcast_spy_returns_correct_value():
    Broadcast()._unheard_messages = []
    assert broadcast_message('info', 'First message') is True
    assert len(Broadcast().spy()) == 1
    assert broadcast_message('info', 'Second message') is True
    assert broadcast_message('info', 'Third message') is True
    assert len(Broadcast().spy()) == 3
    assert Broadcast().listen() is True
    assert len(Broadcast().spy()) == 2


def test_listen_without_messages():
    Broadcast()._unheard_messages = []
    assert Broadcast().listen() is True


def test_listen_with_message(capsys):
    Broadcast()._unheard_messages = []
    broadcast_message('info', 'The answer to life')
    assert Broadcast().listen() is True
    captured = capsys.readouterr()
    assert captured.out == f'{Fore.WHITE}The answer to life{Style.RESET_ALL}\n'


def test_listen_with_invalid_message(capsys, caplog):
    Broadcast()._unheard_messages = [{
        'type': None,
        'message': None,
        'kwargs': None
    }]

    caplog.set_level(logging.DEBUG)

    assert Broadcast().listen() is False
    assert Broadcast().listen() is True
    captured = capsys.readouterr()
    assert captured.out == f'{Fore.RED}Error when trying to listen to a message via Broadcast: ' \
                           f'TypeError("argument of type \'NoneType\' is not iterable"){Style.RESET_ALL}\n'
    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'ERROR'
    caplog.clear()
    assert Broadcast().listen() is True
    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == 'DEBUG'


def test_listen_all_without_messages(capsys):
    Broadcast()._unheard_messages = []
    Broadcast().listen_all()
    captured = capsys.readouterr()
    assert captured.out == ''


def test_listen_all_with_messages(capsys):
    Broadcast()._unheard_messages = []
    broadcast_message('info', 'The answer to life', header=True)
    broadcast_message('info', 'The answer to the universe')
    broadcast_message('echo', 'And everything is 42')
    Broadcast().listen_all()
    captured = capsys.readouterr()
    assert captured.out == f'{Fore.BLUE}The answer to life{Style.RESET_ALL}\n' \
                           f'{Fore.WHITE}The answer to the universe{Style.RESET_ALL}\n' \
                           f'{Fore.WHITE}And everything is 42{Style.RESET_ALL}\n'


def test_broadcast_exception_with_correct_type(capsys):
    Broadcast()._unheard_messages = []
    try:
        raise Exception
    except Exception as e:
        broadcast_message('error', 'Something went wrong', exc=e, unsafe=True)

    assert len(Broadcast().spy()) == 1
    assert Broadcast().listen() is True
    captured = capsys.readouterr()
    assert captured.out == f'{Fore.RED}Something went wrong{Style.RESET_ALL}\n'


def test_broadcast_exception_with_incorrect_type_forced_error(capsys):
    Broadcast()._unheard_messages = []
    try:
        raise Exception
    except Exception as e:
        broadcast_message('info', 'Something went wrong', exc=e, unsafe=True)

    assert len(Broadcast().spy()) == 1
    assert Broadcast().listen() is True
    captured = capsys.readouterr()
    assert captured.out == f'{Fore.RED}Something went wrong{Style.RESET_ALL}\n'


def test_create_subscription():
    listener = Broadcast().subscribe()
    assert listener.daemon is True
    assert hasattr(listener, 'start')
    assert type(listener) == Thread

