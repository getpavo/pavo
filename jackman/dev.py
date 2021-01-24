import shutil
import logging

import socketserver
import http.server
import webbrowser

from jackman.build import Builder
from jackman.helpers import get_cwd, set_dir

log = logging.getLogger(__name__)


def main():
    """Starts a local server that shows you your website in development
    """
    log.info('Starting a temporary build with mode "development"')
    builder = Builder('development')
    builder.build()
    serve_forever(f'{get_cwd()}/{builder.tmp_dir}')


def serve_forever(directory, port=8000):
    log.debug(f'Moving into {directory}')
    if not set_dir(directory):
        raise FileNotFoundError(f'{directory} does not exist')

    tcp_handler = http.server.SimpleHTTPRequestHandler
    socketserver.TCPServer.allow_reuse_address = True
    log.debug(f'Created TCP Handler http.server.SimpleHTTPRequestHandler')

    with socketserver.TCPServer(("", port), tcp_handler) as dev_server:
        try:
            log.info(f'Serving forever on localhost:{port}')
            webbrowser.open(f'http://localhost:{port}')
            dev_server.serve_forever()
        except KeyboardInterrupt:
            log.debug('Detected KeyboardInterrupt. Telling server to shutdown.')
            dev_server.shutdown()
            dev_server.server_close()
            dev_server.socket.close()
            log.info('Successfully closed the server.')
            shutil.rmtree(directory)
            log.debug(f'Removed temporary directory {directory}')
        except Exception as e:
            log.exception(e)
            shutil.rmtree(directory)
            log.debug(f'Removed temporary directory {directory}')

