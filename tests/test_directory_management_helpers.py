import os
import jackman.core
from jackman.helpers.files import get_cwd, set_dir, cd_is_project, get_jackman_dir, force_create_empty_directory, \
    load_files


def test_get_cwd():
    assert get_cwd() == os.getcwd()


def test_set_dir_not_exists(tmpdir):
    assert set_dir(f'{tmpdir}/unknown/') is False


def test_set_dir_exists(tmpdir):
    tmpdir.mkdir('existing-folder')
    assert set_dir(f'{tmpdir}/existing-folder/') is True


def test_force_create_empty_directory_dir_not_exists(tmpdir):
    assert set_dir(f'{tmpdir}/new/') is False
    force_create_empty_directory(f'{tmpdir}/new')
    assert set_dir(f'{tmpdir}/new/') is True


def test_force_create_empty_directory_dir_exists(tmpdir):
    f = tmpdir.mkdir('new').join('.jackman')
    f.write('empty')
    assert set_dir(f'{tmpdir}/new/') is True
    assert cd_is_project() is True
    force_create_empty_directory(f'{tmpdir}/new')
    assert set_dir(f'{tmpdir}/new/') is True
    assert cd_is_project() is False


def test_is_jackman_project_false(tmpdir):
    set_dir(tmpdir)
    assert cd_is_project() is False


def test_is_jackman_project_true(tmpdir):
    f = tmpdir.mkdir('project').join('.jackman')
    f.write('empty')
    set_dir(f'{tmpdir}/project')
    assert cd_is_project() is True


def test_get_jackman_directory():
    assert os.path.dirname(os.path.abspath(jackman.helpers.__file__)) == get_jackman_dir()


def test_load_files_from_empty_directory(tmpdir):
    tmpdir.mkdir('project')
    assert load_files(f'{tmpdir}/project') == {}


def test_load_files_from_directory(tmpdir):
    f = tmpdir.mkdir('project').join('.jackman')
    f.write('empty')
    files = load_files(f'{tmpdir}/project')
    assert len(files) == 1
    assert '.jackman' in files
    assert 'empty' not in files
