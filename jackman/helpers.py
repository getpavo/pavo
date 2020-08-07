import os

from colorama import Fore, Style
import time


# Directory management
def get_cwd():
    return os.getcwd()


def get_sd():
    return os.path.dirname(os.path.abspath(__file__))


def set_dir(directory):
    try:
        os.chdir(str(directory))
        return True
    except OSError:
        return False


def cd_is_project():
    if os.path.isfile('_jackman_config.yaml') or os.path.isfile('_jackman_config.yml'):
        return True
    return False


def log(message, sort='message'):
    sort = sort.lower()
    prefix = {
        'error': Fore.RED,
        'warning': Fore.YELLOW,
        'success': Fore.LIGHTGREEN_EX
    }
    if sort in prefix:
        prefix = prefix[sort]
    else:
        prefix = Fore.LIGHTBLUE_EX

    suffix = Style.RESET_ALL
    if sort == 'error':
        prefix = Fore.RED
    elif sort == 'warning':
        prefix = Fore.YELLOW
    elif sort == 'success':
        prefix = Fore.LIGHTGREEN_EX

    current_time = time.strftime('%H:%M:%S')

    print(f'{prefix}[{current_time}] {message}{suffix}')
