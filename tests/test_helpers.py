import pytest
import os

from jackman.helpers import *


class TestExpectsContextManager:
    def test_expects_input_not_list(self):
        with pytest.raises(ValueError):
            with Expects(KeyError):
                raise Exception

    def test_expects_catch_error(self):
        with Expects([ZeroDivisionError]):
            print(10 / 0)

    def test_expects_catch_error_multiple(self):
        with Expects([ZeroDivisionError, KeyError]):
            print(10 / 0)

    def test_expects_no_error(self):
        with Expects([KeyError]):
            a = 2
            b = 4
            c = a * b + 10
            print(c)

        assert c == 18


class TestDirectoryManagement:
    def test_get_cwd(self):
        assert get_cwd() == os.getcwd()

    def test_set_dir_not_exists(self, tmpdir):
        assert set_dir(f'{tmpdir}/unknown/') is False

    def test_set_dir_exists(self, tmpdir):
        tmpdir.mkdir('existing-folder')
        assert set_dir(f'{tmpdir}/existing-folder/') is True

    def test_is_jackman_project_false(self, tmpdir):
        set_dir(tmpdir)
        assert cd_is_project() is False

    def test_is_jackman_project_true(self, tmpdir):
        f = tmpdir.mkdir('project').join('_jackman_config.yaml')
        f.write('empty')
        set_dir(f'{tmpdir}/project')
        assert cd_is_project() is True


class TestYaml:
    pass
