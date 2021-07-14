import shutil
import os
from httpwatcher import HttpWatcherServer
from tornado.ioloop import IOLoop
from typing import Union

from .build import Builder

from pova.helpers.files import cd_is_project
from pova.cli.broadcast import broadcast_message


def main() -> None:
    """Starts a local server that shows you your website in development.
    """
    server = DevelopmentServer()
    broadcast_message('info', 'Starting local development server. Awaiting build.', header=True)
    server.run()


class DevelopmentServer:
    def __init__(self) -> None:
        self.builder: Builder = Builder('development')
        self.project_directory: str = os.getcwd() if cd_is_project() else None
        self.directory: str = self.builder.tmp_dir
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
        broadcast_message('info', f'Building to temporary output directory: {self.directory}.')
        self.builder.build()
        self.server.listen()
        broadcast_message('success',
                          f'Local development server opened in browser on {self.server.host}:{self.server.port}.')
        try:
            IOLoop.current().start()
        except KeyboardInterrupt:
            broadcast_message('debug', '', disable_logging=True)
            broadcast_message('warn', 'Detected request to stop server. Please wait.')
            self.server.shutdown()
        finally:
            self._remove_leftovers()

    def _build_temporary_directory(self) -> None:
        broadcast_message('info', 'Detected changes, rebuilding project.', header=True)
        self.builder.build()

    def _remove_leftovers(self) -> None:
        shutil.rmtree(self.directory)
        broadcast_message('info', 'Removed temporary build directory from filesystem.')
        broadcast_message('success', 'Gracefully shut down the local development server.')
