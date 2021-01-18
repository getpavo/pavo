import os
import shutil
import logging

import socketserver
import http.server

from jackman.build import Builder
from jackman.helpers import get_cwd


def serve_local_website():
    logging.getLogger('dev')
    builder = Builder('development')
    builder.build()
    serve_forever(f'{get_cwd()}/{builder.tmp_dir}')


def serve_forever(directory, port=8000):
    # TODO: Add handler for server stop on KeyboardInterrupt
    # TODO: Move this to another file
    os.chdir(directory)
    TCPHandler = http.server.SimpleHTTPRequestHandler
    socketserver.TCPServer.allow_reuse_address = True

    with socketserver.TCPServer(("", port), TCPHandler) as dev_server:
        try:
            dev_server.serve_forever()
        except KeyboardInterrupt:
            dev_server.shutdown()
            dev_server.server_close()
            dev_server.socket.close()
            shutil.rmtree(directory)
        except Exception as e:
            logging.exception(e)
            shutil.rmtree(directory)
