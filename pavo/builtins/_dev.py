import os
import atexit
from typing import Union, Optional
from tempfile import TemporaryDirectory
from dataclasses import dataclass

# TODO: replace this, broken in Python 3.10 - See the QSDS project.
# from httpwatcher import HttpWatcherServer
from tornado.ioloop import IOLoop

from pavo.ddl.commands import CommandInterface
from pavo.ddl.messages import MessageHandlerInterface
from ._build import Builder


@dataclass
class Dev(CommandInterface):
    name: str = 'dev'
    help: str = 'Starts the development preview server.'
    allow_outside_project: bool = False

    def run(self, args: Optional[list] = None) -> None:
        with TemporaryDirectory() as tmp_dir:
            msg_handler, *_ = self.injected
            server = DevelopmentServer(tmp_dir, msg_handler)
            msg_handler.print(
                'info',
                'Starting local development server. Awaiting build.',
                header=True
            )
            server.run()


class DevelopmentServer:
    """Containing class for the development server used in Pavo projects.

    Args:
        build_directory (str): The directory to temporarily keep the build in.

    Attributes:
        builder (Builder): The builder that is used to build the website that will be served to the user.
        project_directory (str): The project directory to monitor for changes.
        directory (str): The location of the temporary directory of the builder, used to serve files from.
        paths_to_watch (list): The paths to watch for any changes in files.
        server_settings (dict): Configuration settings that run the httpwatcher server.
        server (HttpWatcherServer): The actual server that does the heavy work, serving content to the user.
    """

    def __init__(self, build_directory: str, msg_handler: MessageHandlerInterface) -> None:
        self.builder: Builder = Builder(build_directory, msg_handler)
        self.project_directory: str = os.getcwd()
        self.directory: str = self.builder.tmp_dir
        self.msg_handler: MessageHandlerInterface = msg_handler
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

        atexit.register(self.msg_handler.print, 'success', 'Shut down development server.')

        self.server: HttpWatcherServer = HttpWatcherServer(
            self.directory,
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
        self.builder.build(False)
        self.server.listen()
        self.msg_handler.print('success',
                       f'Local development server opened in browser on {self.server.host}:{self.server.port}.')
        try:
            IOLoop.current().start()
        except KeyboardInterrupt:
            self.msg_handler.print('debug', '', disable_logging=True)
            self.msg_handler.print('warn', 'Detected request to stop server. Please wait.')
            self.server.shutdown()

    def _build_temporary_directory(self) -> None:
        """Triggers a build to the temporary directory on detection of changes to the project."""
        self.msg_handler.print('info', 'Detected changes, rebuilding project.', header=True)
        self.builder.build(False)
