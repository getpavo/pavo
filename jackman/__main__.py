#!/usr/bin/env python3
import logging
import argparse
import os

import http.server
import socketserver

from distutils.dir_util import copy_tree
from colorama import init

from jackman.errors import *
from jackman.helpers import get_cwd, get_jackman_dir, set_dir, cd_is_project, setup_logging
from jackman.builder import Builder


class Jackman(object):
    def __init__(self):
        init()
        setup_logging()

        self.argument_parser = self.create_parser()
        self.arguments = vars(self.argument_parser.parse_args())
        self.logger = logging.getLogger('jackman.core')

    def execute(self, command=None):
        try:
            command = self.arguments['command'][0]
        except KeyError:
            self.logger.exception('Executed jackman without specifying a command.')

        self.logger.debug(f'Executing {command}')

        if command != 'create' and not cd_is_project():
            self.logger.critical(f'Directory {os.getcwd()} is not a Jackman project.')
            raise UnknownProjectError

        if command == 'create':
            try:
                self.new_project(self.arguments['command'][1])
            except IndexError:
                self.new_project()

        elif command == 'build':
            self.build()

        elif command == 'dev':
            self.build()
            self.serve()

        elif command == 'deploy':
            pass

        else:
            raise UnknownCliCommandError('Could not execute specified command. It does not exist.')

    @staticmethod
    def create_parser():
        p = argparse.ArgumentParser(description="Work with Jackman via command line interface",
                                    epilog="For more information, please refer to the documentation.")
        p.add_argument('command', metavar='CMD', help='The command Jackman should execute.', nargs='+')
        p.add_argument('--verbose', '-v', help='Whether or not to log actions to the console.', action='store_true')

        return p

    @staticmethod
    def build():
        site = Builder()
        site.build()

    @staticmethod
    def serve():
        os.chdir(f'{get_cwd()}/_website/')
        Handler = http.server.SimpleHTTPRequestHandler

        with socketserver.TCPServer(("", 8000), Handler) as tmp_server:
            tmp_server.serve_forever()


    def new_project(self, name='jackman-project'):
        if os.path.exists(name) and os.path.isdir(name) and len(os.listdir(name)) != 0:
            raise FileExistsError('The specified directory already exists and contains files.')

        try:
            os.mkdir(name)
        except FileExistsError:
            pass

        copy_tree(f'{get_jackman_dir()}/_templates/empty_project/', name)


if __name__ == '__main__':
    cwd = set_dir(get_cwd())
    app = Jackman()
    app.execute()
