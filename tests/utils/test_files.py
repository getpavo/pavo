import os
import pytest
import pathlib

from pavo.utils import files, config


def test_set_dir(monkeypatch) -> None:
    # Successfully change a directory, should return True
    monkeypatch.setattr(os, "chdir", lambda _: None)
    assert files.set_dir("/whatever/test/") is True

    # When an OSError is raised, it should return False
    monkeypatch.setattr(os, "chdir", lambda _: (_ for _ in ()).throw(OSError()))
    assert files.set_dir("/whatever/test/") is False

    # Any other errors should be re-raised
    monkeypatch.setattr(
        os, "chdir", lambda _: (_ for _ in ()).throw(NotImplementedError())
    )
    with pytest.raises(NotImplementedError):
        files.set_dir("/test/")


def test_force_create_empty_directory(tmp_path) -> None:
    pathlib.Path(f"{tmp_path}/remove_me/").mkdir()
    pathlib.Path(f"{tmp_path}/remove_me/.gitkeep").touch()
    assert pathlib.Path(f"{tmp_path}/remove_me/.gitkeep").exists() is True
    files.force_create_empty_directory(f"{tmp_path}/remove_me/")
    assert pathlib.Path(f"{tmp_path}/remove_me/.gitkeep").exists() is False


def test_is_project(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    assert files.cd_is_project() is False
    pathlib.Path(f"{tmp_path}/pavoconfig.yaml").touch()
    assert files.cd_is_project() is True


def test_load_files(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        os,
        "listdir",
        lambda _: [
            f"{tmp_path}/test/whatever",
            f"{tmp_path}/test2",
            f"{tmp_path}/../outside",
        ],
    )
    assert files.load_files(str(tmp_path)) == {
        f"{tmp_path}/test/whatever": "test/whatever",
        f"{tmp_path}/test2": "test2",
        f"{tmp_path}/../outside": "../outside",
    }


def test_convert_md_to_html(monkeypatch) -> None:
    monkeypatch.setattr(config, "get_config_value", lambda _: [])
    assert files.convert_md_to_html("# Test") == "<h1>Test</h1>"
    assert files.convert_md_to_html("---") == "<hr />"
