import logging
import logging.config
import os

import htmlmin
import yaml

log = logging.getLogger(__name__)


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


def setup_logging():
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


def minify_html(html):
    # TODO: Make settings for minifying customizable
    minified_html = htmlmin.minify(html,
                                   remove_comments=True,
                                   remove_empty_space=True,
                                   remove_all_empty_space=False,
                                   reduce_empty_attributes=True,
                                   reduce_boolean_attributes=False,
                                   remove_optional_attribute_quotes=True,
                                   convert_charrefs=True,
                                   keep_pre=False
                                   )
    return minified_html


class Expects(object):
    """
    Context manager when we are expecting that an error could occur and we accept this.
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
