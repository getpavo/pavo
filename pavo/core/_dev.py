import os
import atexit
from typing import Union
from tempfile import TemporaryDirectory

from httpwatcher import HttpWatcherServer
from tornado.ioloop import IOLoop
from pavo.cli import handle_message

from ._build import Builder


def main() -> None:
    """Starts a local server that shows you your website in development.
    TODO: Temporary directory requires a rework, using TemporaryDirectory class  pylint: disable=fixme
    """
    server = DevelopmentServer()
    handle_message('info', 'Starting local development server. Awaiting build.', header=True)
    server.run()


class DevelopmentServer:
    """Containing class for the development server used in Pavo projects.

    Attributes:
        builder (Builder): The builder that is used to build the website that will be served to the user.
        project_directory (str): The project directory to monitor for changes.
        directory (str): The location of the temporary directory of the builder, used to serve files from.
        paths_to_watch (list): The paths to watch for any changes in files.
        server_settings (dict): Configuration settings that run the httpwatcher server.
        server (HttpWatcherServer): The actual server that does the heavy work, serving content to the user.
    """

    def __init__(self) -> None:
        self.builder: Builder = Builder()
        self.project_directory: str = os.getcwd()
        self.directory: TemporaryDirectory = self.builder.tmp_dir
        self.paths_to_watch: list[str] = [
            f'{self.project_directory}/_data/',
            f'{self.project_directory}/_pages/',
            f'{self.project_directory}/_posts/',
            f'{self.project_directory}/_static/templates',
            f'{self.project_directory}/_static/styles'
        ]

        self.server_settings: dict[str, Union[str, int]] = {
            'ip': '127.0.0.1',
            'port': 5556
        }

        atexit.register(self.remove_leftovers)

        self.server: HttpWatcherServer = HttpWatcherServer(
            self.directory.name,
            watch_paths=self.paths_to_watch,
            on_reload=self._build_temporary_directory,
            host=self.server_settings['ip'],
            port=self.server_settings['port'],
            watcher_interval=1.0,
            recursive=True,
            open_browser=True
        )

    def run(self) -> None:
        """Starts a development server and initiates the first build."""
        handle_message('info', f'Building to temporary output directory: {self.directory.name}.')
        self.builder.build(False)
        self.server.listen()
        handle_message('success',
                       f'Local development server opened in browser on {self.server.host}:{self.server.port}.')
        try:
            IOLoop.current().start()
        except KeyboardInterrupt:
            handle_message('debug', '', disable_logging=True)
            handle_message('warn', 'Detected request to stop server. Please wait.')
            self.server.shutdown()

    def _build_temporary_directory(self) -> None:
        """Triggers a build to the temporary directory on detection of changes to the project."""
        handle_message('info', 'Detected changes, rebuilding project.', header=True)
        self.builder.build(False)

    def remove_leftovers(self) -> None:
        """Removes the temporary build directory from the file system."""
        self.directory.cleanup()
        handle_message('success', 'Shut down development server. Removed temporary build directory from filesystem.')
