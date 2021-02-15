import shutil
import logging

import socketserver
import http.server
import webbrowser

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from jackman.build import Builder
from jackman.helpers import get_cwd, set_dir, cd_is_project

log = logging.getLogger(__name__)


def main():
    """Starts a local server that shows you your website in development.
    """
    try:
        server = DevelopmentServer()
        server.run()
    except KeyboardInterrupt:
        print('\nDone')


class DevelopmentServer:
    def __init__(self):
        self.server = None
        self.port = 8000
        self.builder = Builder('development')
        self.directory = self.builder.tmp_dir
        self.project_directory = get_cwd() if cd_is_project() else None
        self.observer = Observer()
        self.handler = DevelopmentServerFileHandler(self.project_directory, self.build_temporary_directory)

    def run(self):
        self.build_temporary_directory()
        self.observer.schedule(self.handler, self.project_directory, recursive=True)
        self.observer.start()
        try:
            self.serve_forever()
        except KeyboardInterrupt:
            self.shutdown()
        self.observer.join()

    def shutdown(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            self.observer.stop()
            log.debug('Successfully closed the server.')
            shutil.rmtree(f'{self.project_directory}/{self.directory}')
            log.debug(f'Removed temporary directory {self.directory}')

    def serve_forever(self):
        """Serve a specified directory until interrupted.

        Raises:
            FileNotFoundError: The specified directory to serve does not exist or is not accessible.
        """
        log.debug(f'Moving into {self.directory}')
        if not set_dir(self.directory):
            raise FileNotFoundError(f'{self.directory} does not exist')

        tcp_handler = http.server.SimpleHTTPRequestHandler
        socketserver.TCPServer.allow_reuse_address = True
        log.debug(f'Created TCP Handler http.server.SimpleHTTPRequestHandler')

        with socketserver.TCPServer(("", self.port), tcp_handler) as dev_server:
            try:
                self.server = dev_server
                log.debug(f'Serving forever on localhost:{self.port}')
                webbrowser.open(f'http://localhost:{self.port}')
                self.server.serve_forever()
            except KeyboardInterrupt:
                self.shutdown()
                dev_server.shutdown()
            except Exception as e:
                self.shutdown()
                raise e from None

    def build_temporary_directory(self):
        log.debug('Starting a temporary build with mode "development"')
        self.builder.build()


class DevelopmentServerFileHandler(FileSystemEventHandler):
    def __init__(self, directory, callback):
        super().__init__()

        # Paths that contain files that when modified should trigger a reload and rebuild
        self.paths = [
            f'{directory}/_pages/',
            f'{directory}/_posts/',
            f'{directory}/_templates',
        ]

        if hasattr(callback, '__call__'):
            self.callback = callback
        else:
            raise TypeError('Callback for DevelopmentServerHandler should be a callable function.')

    def on_any_event(self, event):
        if not event.is_directory and not event.event_type == 'created':
            for path in self.paths:
                if event.src_path.startswith(path):
                    print(event)
                    print('Detected changes, reloading...')
                    self.callback()
