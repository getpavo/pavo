import logging
import logging.config
import os
from functools import reduce
from shutil import rmtree

import yaml

log = logging.getLogger(__name__)


# Directory management checks
def get_cwd():
    """Retrieves the current working directory.

    Returns:
        str: The path to the current working directory.
    """
    return os.getcwd()


def get_jackman_dir():
    """Retrieves the path to the installation folder of the Jackman module.

    Returns:
        str: The path to the jackman module folder.
    """
    return os.path.dirname(os.path.abspath(__file__))


def set_dir(directory):
    """Changes the current directory to the specified directory.

    Args:
        directory (str): The path to the directory to change the working directory to.

    Returns:
        bool: Whether or not changing the directory was successful.
    """
    try:
        os.chdir(str(directory))
        return True
    except OSError:
        return False


def force_create_empty_directory(directory):
    """Forcefully creates an empty directory, even when it already exists.

    Args:
        directory (str): The path to the directory that needs to be created.

    Warning:
        This command always creates a new directory on the path. Only use it if you are sure that you can trust the
        function input. In all other cases, please use os.mkdir and catch the exception yourself.
    """
    try:
        os.mkdir(directory)
    except FileExistsError:
        rmtree(directory)
        os.mkdir(directory)


def cd_is_project():
    """Checks whether or not the current directory is a Jackman project.

    Returns:
        bool: Whether or not the current directory is an initialized Jackman project.
    """
    return os.path.isfile('.jackman')


def load_files(path):
    """Indexes files in a path and loads them into a dict.

    Args:
        path (str): The path to the file that should be loaded into a dict.

    Returns:
          dict: All filenames in the specified path.
    """
    files = {}
    for file in os.listdir(path):
        files[file] = os.path.relpath(file)

    return files


def get_config_value(keys):
    """Retrieves a configuration value from the Jackman configuration file.

    Args:
        keys (str): The string of (nested) dictionary values.

    Note:
        You can find nested keys by introducing '.' in your ``keys`` value.
        foo.bar will be looked up as: ``config[foo][bar]``

    Returns:
        dict/str: Dictionary with values if not fully nested, string with value if fully unnested.
    """
    with open('.jackman', 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    return reduce(lambda d, key: d.get(key, '') if isinstance(d, dict) else '', keys.split("."), config)


class Expects(object):
    """Context manager when we are expecting that an error could occur and we accept this.

    Args:
        expected_errors (list): A list of expected errors to skip.

    Raises:
        ValueError: The provided argument is not a list.

    Attributes:
        expected_errors (list): A list of expected errors to skip.
    """
    def __init__(self, expected_errors):
        if type(expected_errors) != list:
            raise ValueError('Expected list as list of expected errors')
        self.expected_errors = expected_errors

    def __enter__(self):
        pass

    def __exit__(self, err, value, traceback):
        if not err:
            return True
        if err in self.expected_errors:
            return True
        else:
            raise err


def singleton(class_):
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return get_instance
