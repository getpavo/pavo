import shutil
from httpwatcher import HttpWatcherServer
from tornado.ioloop import IOLoop

from .build import Builder

from jackman.helpers.files import get_cwd, cd_is_project
from jackman.cli.broadcast import broadcast_message


def main():
    """Starts a local server that shows you your website in development.
    """
    server = DevelopmentServer()
    broadcast_message('info', 'Starting local development server. Awaiting build.', header=True)
    server.run()


class DevelopmentServer:
    def __init__(self):
        self.builder = Builder('development')
        self.project_directory = get_cwd() if cd_is_project() else None
        self.directory = self.builder.tmp_dir
        self.paths_to_watch = [
            f'{self.project_directory}/_data/',
            f'{self.project_directory}/_pages/',
            f'{self.project_directory}/_posts/',
            f'{self.project_directory}/_static/templates',
            f'{self.project_directory}/_static/styles'
        ]

        self.server_settings = {
            'ip': '127.0.0.1',
            'port': 5556
        }

        self.server = HttpWatcherServer(
            self.directory,
            watch_paths=self.paths_to_watch,
            on_reload=self._build_temporary_directory,
            host=self.server_settings['ip'],
            port=self.server_settings['port'],
            watcher_interval=1.0,
            recursive=True,
            open_browser=True
        )

    def run(self):
        broadcast_message('info', f'Building to temporary output directory: {self.directory}.')
        self.builder.build()
        self.server.listen()
        try:
            IOLoop.current().start()
        except KeyboardInterrupt:
            self.server.shutdown()
        finally:
            self._remove_leftovers()

    def _build_temporary_directory(self):
        broadcast_message('info', 'Detected changes, rebuilding project.', header=True)
        self.builder.build()

    def _remove_leftovers(self):
        shutil.rmtree(self.directory)
        broadcast_message('info', 'Removed temporary build directory from filesystem.')