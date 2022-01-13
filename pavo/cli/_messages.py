import logging
import sys
from typing import Any, Optional
from colorama import init, Fore, Style

from pavo.helpers import config

log = logging.getLogger('pavo')

try:
    log_level = config.get_config_value('logging.level')
    log.setLevel(log_level if isinstance(log_level, (int, str)) else 20)
    log.disabled = config.get_config_value('logging.enabled') == 'false'

    # Only add a file formatter when the configuration file can be found
    # This ensures that no log file exists outside a Pavo project
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler('pavo.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)
    log.addHandler(file_handler)
    log.propagate = False
except FileNotFoundError:
    log.disabled = True

# Initialize Colorama
init()


def ask(msg: str) -> str:
    """Asks the user for input and returns the value.

    Args:
        msg (str): The input prompt for the user.

    Returns:
        str: The user input.
    """
    return input(f'{Fore.YELLOW}> {msg}{Style.RESET_ALL}')


def debug(msg: str, **kwargs: Any) -> None:
    """Silently logs the message to the debug log.

    Args:
        msg (str): The message that will be shown to the user.
        kwargs: See below.

    Keyword Arguments:
        logger_name (str): Used to override the default 'pavo' name for the logger.
    """
    if 'logger_name' in kwargs:
        alt = logging.getLogger(kwargs['logger_name'])
        alt.debug(msg)
    else:
        log.debug(msg)


def echo(msg: str) -> None:
    """Echo's back the message, without logging it.

    Args:
        msg (str): The message that will be shown to the user.
    """
    print(f'{Fore.WHITE}{msg}{Style.RESET_ALL}')


def info(msg: str, **kwargs: Any) -> None:
    """Shows information about runtime.

    Args:
        msg (str): The message that will be shown to the user.
    """
    if kwargs.get('header', False):
        print(f'{Fore.BLUE}{msg}{Style.RESET_ALL}')
    else:
        print(f'{Fore.WHITE}{msg}{Style.RESET_ALL}')

    if not kwargs.get('disable_logging', False):
        if 'logger_name' in kwargs:
            alt = logging.getLogger(kwargs['logger_name'])
            alt.info(msg)
        else:
            log.info(msg)


def warn(msg: str, **kwargs: Any) -> None:
    """Shows a warning in the console and logs it to the Pavo log.

    Args:
        msg (str): The message that will be shown to the user.
        kwargs: See below.

    Keyword Arguments:
        disable_logging (bool): When set to True, disables the log for a call.
        logger_name (str): Used to override the default 'pavo' name for the logger.
    """
    print(f'{Fore.YELLOW}{msg}{Style.RESET_ALL}')
    if not kwargs.get('disable_logging', False):
        if 'logger_name' in kwargs:
            alt = logging.getLogger(kwargs['logger_name'])
            alt.warning(msg)
        else:
            log.warning(msg)


def error(msg: str, exc: Optional[Exception] = None, **kwargs: Any) -> None:
    """Prints an error message to the terminal and, if provided, logs the exception.

    Args:
        msg (str): The message that will be shown to the user.
        exc (Exception): The exception that was caught and lead to this error message.
        kwargs: See below.

    Keyword Arguments:
        disable_logging (bool): When set to True, disables the log for a call.
        logger_name (str): Used to override the default 'pavo' name for the logger.
        unsafe (bool): When set to True, does not exist the program after catching error.
    """
    print(f'{Fore.RED}{msg}{Style.RESET_ALL}')

    if not kwargs.get('disable_logging', False) and exc is not None:
        if 'logger_name' in kwargs:
            alt = logging.getLogger(kwargs['logger_name'])
            alt.exception(exc)
        else:
            log.exception(exc)
    if 'unsafe' not in kwargs or kwargs['unsafe'] is False:
        sys.exit()


def success(msg: str, **kwargs: Any) -> None:
    """Prints a green success message to the terminal and logs it.

    Args:
        msg (str): The message that will be shown to the user.
        kwargs: See below.

    Note:
        The success log will be of type 'info'.

    Keyword Arguments:
        disable_logging (bool): When set to True, disables the log for a call.
        logger_name (str): Used to override the default 'pavo' name for the logger.
        disable_checkmark (bool): Whether to show a checkmark with the success message.
    """
    if kwargs.get('disable_checkmark', False):
        print(f'{Fore.GREEN}{msg}{Style.RESET_ALL}')
    else:
        print(f'{Fore.GREEN}\u2713 {msg}{Style.RESET_ALL}')

    if not kwargs.get('disable_logging', False):
        if 'logger_name' in kwargs:
            alt = logging.getLogger(kwargs['logger_name'])
            alt.info(msg)
        else:
            log.info(msg)
