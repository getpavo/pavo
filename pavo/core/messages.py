import logging
from typing import Optional

# TODO: Swap colorama for Rich. pylint: ignore=fixme
import colorama

from pavo.utils import config

_log_level: int = 20
_logger = logging.getLogger("pavo")
try:
    _log_level = config.get_config_value("logging.level")
    _logger.disabled = config.get_config_value("logging.enabled") == "false"

    # Ensures no logging takes place into files outside of a Pavo project
    # TODO: Rework this to log into a regular log folder, instead of project folder. pylint: ignore=fixme
    _file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    _file_handler = logging.FileHandler("pavo.log", delay=True)
    _file_handler.setLevel(logging.DEBUG)
    _file_handler.setFormatter(_file_formatter)
    _logger.addHandler(_file_handler)
    _logger.propagate = False
except FileNotFoundError:
    _logger.disabled = True
finally:
    _logger.setLevel(_log_level if isinstance(_log_level, (int, str)) else 20)


def echo(message: str) -> None:
    print(f"{colorama.Fore.WHITE}{message}{colorama.Style.RESET_ALL}")


def header(message: str) -> None:
    _logger.log(logging.INFO, message)
    print(f"{colorama.Fore.BLUE}{message}{colorama.Style.RESET_ALL}")


def info(message: str) -> None:
    _logger.log(logging.INFO, message)
    print(f"{colorama.Fore.WHITE}{message}{colorama.Style.RESET_ALL}")


def ask(message: str) -> str:
    _logger.log(logging.DEBUG, 'Requested input from user with message: "%s"', message)
    response = input(f"{colorama.Fore.YELLOW}> {message}{colorama.Style.RESET_ALL}")
    _logger.log(logging.DEBUG, 'Received user input: "%s"', response)
    return response


def debug(message: str) -> None:
    _logger.log(logging.DEBUG, message)


def warning(message: str) -> None:
    _logger.log(logging.WARNING, message)
    print(f"{colorama.Fore.YELLOW}WARNING: {message}{colorama.Style.RESET_ALL}")


def error(message: str, err: Optional[BaseException] = None) -> None:
    _logger.log(logging.ERROR, message)
    print(f"{colorama.Fore.RED}ERROR: {message}{colorama.Style.RESET_ALL}")

    if err is not None:
        _logger.log(logging.ERROR, err)
        print(f"{colorama.Fore.RED}{repr(err)}{colorama.Style.RESET_ALL}")


def success(message: str) -> None:
    _logger.log(logging.INFO, message)
    print(f"{colorama.Fore.GREEN}\u2713 {message}{colorama.Style.RESET_ALL}")
