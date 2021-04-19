import shutil
import logging
from httpwatcher import HttpWatcherServer
from tornado.ioloop import IOLoop

from jackman.core.build import Builder
from jackman.core.helpers import get_cwd, set_dir, cd_is_project

log = logging.getLogger(__name__)


def main():
    """Starts a local server that shows you your website in development.
    """
    server = DevelopmentServer()
    server.run()


class DevelopmentServer:
    def __init__(self):
        self.builder = Builder('development')
        self.project_directory = get_cwd() if cd_is_project() else None
        self.directory = self.builder.tmp_dir
        self.paths_to_watch = [
            f'{self.project_directory}/_pages/',
            f'{self.project_directory}/_posts/',
            f'{self.project_directory}/_templates',
        ]

        self.server_settings = {
            'ip': '127.0.0.1',
            'port': 5556
        }

        self.server = HttpWatcherServer(
            self.directory,
            watch_paths=self.paths_to_watch,
            on_reload=self.build_temporary_directory,
            host=self.server_settings['ip'],
            port=self.server_settings['port'],
            watcher_interval=1.0,
            recursive=True,
            open_browser=True
        )

    def run(self):
        self.build_temporary_directory()
        self.server.listen()
        try:
            IOLoop.current().start()
        except KeyboardInterrupt:
            self.server.shutdown()
            self.remove_leftovers()

    def build_temporary_directory(self):
        log.debug('Starting a temporary build with mode "development"')
        self.builder.build()

    def remove_leftovers(self):
        shutil.rmtree(self.directory)
        log.debug(f'Removed temporary development server directory {self.directory}')
