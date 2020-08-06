#!/usr/bin/env python3

import argparse
import os

from distutils.dir_util import copy_tree


from errors import *
from helpers import get_cwd, get_sd, set_dir


def create_parser():
    p = argparse.ArgumentParser(description="Work with Jackman via command line interface",
                                epilog="For more information, please refer to the documentation.")
    p.add_argument('command', metavar='CMD', help='The command Jackman should execute.', nargs='+')
    p.add_argument('--verbose', '-v', help='Whether or not to log actions to the console.', action='store_true')

    return p


def _new_jackman_workspace(name='jackman-project'):
    if os.path.exists(name) and os.path.isdir(name) and len(os.listdir(name)) != 0:
        raise FileExistsError('The specified directory already exists and contains files.')

    try:
        os.mkdir(name)
    except FileExistsError:
        pass

    copy_tree(f'{get_sd()}/templates/empty_project/', f'{get_cwd()}/{name}')


if __name__ == '__main__':
    cwd = set_dir(get_cwd())
    parser = create_parser()
    args = vars(parser.parse_args())
    command = args['command'][0]

    if command == 'create':
        try:
            _new_jackman_workspace(args['command'][1])
        except IndexError:
            _new_jackman_workspace()

    elif command == 'build':
        pass
    elif command == 'preview':
        pass
    elif command == 'deploy':
        pass
    else:
        raise UnknownCliCommandError('Could not execute specified command. It does not exist.')
