import logging
from colorama import init, Fore, Style


# Set up logging
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('jackman.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(file_formatter)

logging.basicConfig(level=logging.DEBUG, handlers=[file_handler])
log = logging.getLogger('jackman')

# Initialize Colorama
init()


def empty():
    print('')


def debug(msg, **kwargs):
    """Silently logs the message to the debug log."""
    if 'logger_name' in kwargs:
        alt = logging.getLogger(kwargs['logger_name'])
        alt.debug(msg)
    else:
        log.debug(msg)


def echo(msg):
    """Echo's back the message, without logging it."""
    print(f'{Fore.WHITE}{msg} {Style.RESET_ALL}')


def info(msg, **kwargs):
    """Shows information about runtime and logs it to the Jackman log."""
    print(f'{Fore.BLUE}{msg} {Style.RESET_ALL}')
    if 'disable_logging' not in kwargs or kwargs['disable_logging'] is False:
        if 'logger_name' in kwargs:
            alt = logging.getLogger(kwargs['logger_name'])
            alt.info(msg)
        else:
            log.info(msg)


def warn(msg, **kwargs):
    """Shows a warning in the console and logs it to the Jackman log."""
    print(f'{Fore.YELLOW}{msg} {Style.RESET_ALL}')
    if 'disable_logging' not in kwargs or kwargs['disable_logging'] is False:
        if 'logger_name' in kwargs:
            alt = logging.getLogger(kwargs['logger_name'])
            alt.warning(msg)
        else:
            log.warning(msg)


def error(msg, exc=None, **kwargs):
    """Prints an error message to the terminal and, if provided, logs the exception.

    Args:
        msg (str): The message that will be shown to the user.
        exc (Exception): The exception that was caught and lead to this error message.
        kwargs: See below

    Keyword Arguments:
        disable_logging (bool): When set to True, disables the log for a call.
        logger_name (str): Used to override the default 'jackman' name for the logger.
        unsafe (bool): When set to True, does not exist the program after catching error.
    """
    print(f'{Fore.RED}{msg}{Style.RESET_ALL}')

    if 'disable_logging' not in kwargs or kwargs['disable_logging'] is False and exc is not None:
        if 'logger_name' in kwargs:
            alt = logging.getLogger(kwargs['logger_name'])
            alt.exception(exc)
        else:
            log.exception(exc)
    if 'unsafe' not in kwargs or kwargs['unsafe'] is False:
        exit()
