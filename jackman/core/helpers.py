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

    Raises:
        ValueError: No directory was specified.

    Returns:
        bool: Whether or not changing the directory was successful.
    """
    if not directory:
        raise ValueError('Missing directory.')

    try:
        os.chdir(str(directory))
        return True
    except OSError:
        return False


def create_empty_directory(directory):
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


def setup_logging():
    """Sets up default logging, so we can streamline it across multiple modules.

    Returns:
        None
    """
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_formatter = logging.Formatter('%(levelname)s - %(message)s')

    file_handler = logging.FileHandler('jackman.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.WARNING)
    stream_handler.setFormatter(stream_formatter)

    logging.basicConfig(level=logging.DEBUG, handlers=[file_handler, stream_handler])


def load_yaml(file):
    """Loads the content of a yaml-file into a dictionary.

    Args:
        file (str): The path to the file that should be loaded.

    Returns:
        dict: A dict with all the items in the yaml-file.
    """
    if not is_yaml(file):
        log.error(f'Unable to read data from "{file}". It is not a yaml-file.')
        return {}
    try:
        with open(file, 'r') as f:
            items = yaml.load(f, Loader=yaml.FullLoader)
            return items
    except FileNotFoundError as e:
        log.exception(e, exc_info=False)
        return {}


def is_yaml(file):
    """Checks whether or not the specified file is a yaml-file.

    Args:
        file (str): The relative path to the file that should be checked.

    Returns:
        bool: Whether or not the specified file is a yaml-file.
    """
    if file.endswith('.yaml') or file.endswith('.yml'):
        return True
    return False


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
    config = {}
    try:
        config = load_yaml('_jackman_config.yaml')
    except FileNotFoundError:
        log.exception('Missing configuration file, are you sure _jackman_config.yaml exists?')
    finally:
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
