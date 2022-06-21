import os
import shutil
import markdown2

from ._config import get_config_value


def set_dir(directory: str) -> bool:
    """Changes the current directory to the specified directory.

    Args:
        directory (str): The path to the directory to change the working directory to.

    Returns:
        bool: Whether changing the directory was successful.
    """
    try:
        os.chdir(str(directory))
        return True
    except OSError:
        return False


def force_create_empty_directory(directory: str) -> None:
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
        shutil.rmtree(directory)
        os.mkdir(directory)


def cd_is_project() -> bool:
    """Checks whether the current directory is a Pavo project.

    Returns:
        bool: Whether the current directory is an initialized Pavo project.
    """
    return os.path.isfile("pavoconfig.yaml")


def load_files(path: str) -> dict[str, str]:
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


def convert_md_to_html(markdown: str) -> str:
    """Translates raw markdown into ready html code.

    This method uses the markdown build configuration value in the pavoconfig.yaml file, which tells this method
    what extras to use when building. (Default: fenced code blocks and cuddled lists)

    Args:
        markdown (str): The Markdown code to be translated to HTML.

    Returns:
        str: The html that was built from the markdown.
    """
    html = markdown2.markdown(
        markdown, extras=get_config_value("build.markdown.extras")
    )
    html = html.replace("\n\n", "\n").rstrip()

    return str(html)
