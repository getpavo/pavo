import os
import shutil
import logging

import socketserver
import http.server

from jackman.build import Builder
from jackman.helpers import get_cwd

log = logging.getLogger(__name__)


def serve_local_website():
    log.info('Starting a temporary build with mode "development"')
    builder = Builder('development')
    builder.build()
    serve_forever(f'{get_cwd()}/{builder.tmp_dir}')


def serve_forever(directory, port=8000):
    log.debug(f'Moving into {directory}')
    os.chdir(directory)

    TCPHandler = http.server.SimpleHTTPRequestHandler
    socketserver.TCPServer.allow_reuse_address = True
    log.debug(f'Created TCP Handler http.server.SimpleHTTPRequestHandler')

    with socketserver.TCPServer(("", port), TCPHandler) as dev_server:
        try:
            log.info(f'Serving forever on localhost:{port}')
            dev_server.serve_forever()
        except KeyboardInterrupt:
            log.debug('Detected KeyboardInterrupt. Telling server to shutdown.')
            dev_server.shutdown()
            dev_server.server_close()
            dev_server.socket.close()
            log.info('Succesfully closed the server.')
            shutil.rmtree(directory)
            log.debug(f'Removed temporary directory {directory}')
        except Exception as e:
            log.exception(e)
            shutil.rmtree(directory)
            log.debug(f'Removed temporary directory {directory}')

