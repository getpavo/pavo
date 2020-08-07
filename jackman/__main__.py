#!/usr/bin/env python3

import argparse
import os

from distutils.dir_util import copy_tree


from errors import *
from helpers import get_cwd, get_sd, set_dir


class Jackman(object):
    def __init__(self):
        self.argument_parser = self.create_parser()
        self.arguments = vars(self.argument_parser.parse_args())

    def execute(self, command=None):
        try:
            command = self.arguments['command'][0]
        except KeyError:
            pass

        if command == 'create':
            try:
                self.new_project(self.arguments['command'][1])
            except IndexError:
                self.new_project()

        elif command == 'build':
            pass
        elif command == 'preview':
            pass
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

    def new_project(self, name='jackman-project'):
        if os.path.exists(name) and os.path.isdir(name) and len(os.listdir(name)) != 0:
            raise FileExistsError('The specified directory already exists and contains files.')

        try:
            os.mkdir(name)
        except FileExistsError:
            pass

        copy_tree(f'{get_sd()}/templates/empty_project/', f'{get_cwd()}/{name}')
        self.__log('', 'success')

    @staticmethod
    def __log(message, sort='Message'):
        print(message)


if __name__ == '__main__':
    cwd = set_dir(get_cwd())
    app = Jackman()
    app.execute()
