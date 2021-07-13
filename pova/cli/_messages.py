import logging
from colorama import init, Fore, Style


# Set up logging
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('pova.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(file_formatter)

log = logging.getLogger('pova')
log.addHandler(file_handler)
log.setLevel(logging.INFO)
log.propagate = False

# Initialize Colorama
init()


def ask(msg):
    """Asks the user for input and returns the value.

    Args:
        msg (str): The input prompt for the user.

    Returns:
        str: The user input.
    """
    return input(f'{Fore.YELLOW}> {msg}{Style.RESET_ALL}')


def debug(msg, **kwargs):
    """Silently logs the message to the debug log.

    Args:
        msg (str): The message that will be shown to the user.
        kwargs: See below.

    Keyword Arguments:
        logger_name (str): Used to override the default 'pova' name for the logger.
    """
    if 'logger_name' in kwargs:
        alt = logging.getLogger(kwargs['logger_name'])
        alt.debug(msg)
    else:
        log.debug(msg)


def echo(msg, **kwargs):
    """Echo's back the message, without logging it.

    Args:
        msg (str): The message that will be shown to the user.
    """
    print(f'{Fore.WHITE}{msg}{Style.RESET_ALL}')


def info(msg, **kwargs):
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


def warn(msg, **kwargs):
    """Shows a warning in the console and logs it to the Pova log.

    Args:
        msg (str): The message that will be shown to the user.
        kwargs: See below.

    Keyword Arguments:
        disable_logging (bool): When set to True, disables the log for a call.
        logger_name (str): Used to override the default 'pova' name for the logger.
    """
    print(f'{Fore.YELLOW}{msg}{Style.RESET_ALL}')
    if not kwargs.get('disable_logging', False):
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
        kwargs: See below.

    Keyword Arguments:
        disable_logging (bool): When set to True, disables the log for a call.
        logger_name (str): Used to override the default 'pova' name for the logger.
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
        exit()


def success(msg, **kwargs):
    """Prints a green success message to the terminal and logs it.

    Args:
        msg (str): The message that will be shown to the user.
        kwargs: See below.

    Note:
        The success log will be of type 'info'.

    Keyword Arguments:
        disable_logging (bool): When set to True, disables the log for a call.
        logger_name (str): Used to override the default 'pova' name for the logger.
        disable_checkmark (bool): Whether or not to show a checkmark with the success message.
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
