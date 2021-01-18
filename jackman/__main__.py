#!/usr/bin/env python3
import logging
import argparse
import os

from distutils.dir_util import copy_tree
from colorama import init

from jackman.errors import *
from jackman.helpers import get_cwd, get_jackman_dir, set_dir, cd_is_project, setup_logging
from jackman.build import Builder
from jackman.dev import serve_local_website


class Jackman(object):
    def __init__(self):
        init()
        setup_logging()

        # TODO: Implement verbose option so we can toggle debug logging
        self.argument_parser = self.create_parser()
        self.arguments = vars(self.argument_parser.parse_args())
        self.logger = logging.getLogger('jackman.core')

    def execute(self, command):
        if command is None:
            command = 'help'

        self.logger.debug(f'Executing {command}')
        is_project = cd_is_project()

        if command != 'create' and not is_project:
            self.logger.critical(f'Directory {os.getcwd()} is not a Jackman project.')
            raise UnknownProjectError

        if command == 'create' and is_project:
            self.logger.critical(f'Directory {os.getcwd()} is already a Jackman project and should not be nested.')

        if command == 'create':
            try:
                self.new_project(self.arguments['command'][1])
            except IndexError:
                self.new_project()

        elif command == 'build':
            self._build()

        elif command == 'dev':
            # TODO: Remove intertwined build and dev serving
            # TODO: Update on finding a change, watching project directory
            serve_local_website()

        elif command == 'deploy':
            pass

        elif command == 'help':
            pass

        else:
            raise UnknownCliCommandError('Could not execute specified command. It does not exist.')

    @staticmethod
    def create_parser():
        p = argparse.ArgumentParser(description="Work with Jackman via command line interface",
                                    epilog="For more information, please refer to the documentation.")
        p.add_argument('command',
                       metavar='COMMAND',
                       help='The command Jackman should execute.',
                       nargs='?')
        p.add_argument('--verbose', '-v',
                       help='Whether or not to log actions to the console.',
                       action='store_true')

        return p

    @staticmethod
    def _build():
        site = Builder()
        site.build()

    @staticmethod
    def new_project(name='jackman-project'):
        if os.path.exists(name) and os.path.isdir(name) and len(os.listdir(name)) != 0:
            raise FileExistsError('The specified directory already exists and contains files.')

        try:
            os.mkdir(name)
        except FileExistsError:
            pass

        copy_tree(f'{get_jackman_dir()}/_templates/empty_project/', name)


if __name__ == '__main__':
    app = Jackman()
    app.execute(app.arguments['command'])
