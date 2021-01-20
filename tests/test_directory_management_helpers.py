import pytest
import os

from jackman.helpers import get_cwd, set_dir, cd_is_project


def test_get_cwd():
    assert get_cwd() == os.getcwd()


def test_set_dir_not_exists(tmpdir):
    assert set_dir(f'{tmpdir}/unknown/') is False


def test_set_dir_exists(tmpdir):
    tmpdir.mkdir('existing-folder')
    assert set_dir(f'{tmpdir}/existing-folder/') is True


def test_is_jackman_project_false(tmpdir):
    set_dir(tmpdir)
    assert cd_is_project() is False


def test_is_jackman_project_true(tmpdir):
    f = tmpdir.mkdir('project').join('_jackman_config.yaml')
    f.write('empty')
    set_dir(f'{tmpdir}/project')
    assert cd_is_project() is True
