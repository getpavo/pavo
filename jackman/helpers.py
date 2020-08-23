import os
import time
import yaml

from colorama import Fore, Style


# Directory management checks
def get_cwd():
    """
    Retrieves the current working directory.

    Returns
    -------
    cwd : str
        The path to the current working directory.
    """
    return os.getcwd()


def get_jackman_dir():
    """
    Retrieves the path to the installation folder of the Jackman module.

    Returns
    -------
    path : str
        The path to the jackman module folder.
    """
    return os.path.dirname(os.path.abspath(__file__))


def set_dir(directory):
    """
    Changes the current directory to the specified directory.

    Parameters
    ----------
    directory : str
        The path to the directory to change to.

    Returns
    -------
    complete : bool
        Whether or not the directory was changed.
    """
    try:
        os.chdir(str(directory))
        return True
    except OSError:
        return False


def cd_is_project():
    """
    Checks whether or not the current directory is a Jackman project.

    Returns
    -------
    project : bool
        Whether or not the current directory can be marked as an initialized jackman project.
    """
    if os.path.isfile('_jackman_config.yaml') or os.path.isfile('_jackman_config.yml'):
        return True
    return False


def log(message, sort='message'):
    # TODO: Rewrite log method to incorporate and use Python logging module
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


def load_yaml(file):
    """
    Loads a yaml-file into a dictionary.

    Parameters
    ----------
    file : str
        The path to the file that should be loaded.

    Returns
    -------
    items : dict
        A dict with all the items in the yaml-file.
    """
    if not is_yaml(file):
        # TODO: This should raise a warning in the logging module.
        return {}

    with open(file, 'r') as f:
        items = yaml.load(f, Loader=yaml.FullLoader)

    return items

def is_yaml(file):
    """
    Checks whether or not the specified file is a yaml-file.

    Parameters
    ----------
    file : str
        The relative path to the file that should be checked.

    Returns
    -------
    bool
        Whether or not the specified file is a yaml-file.
    """
    if file.endswith('.yaml') or file.endswith('.yml'):
        return True
    return False
