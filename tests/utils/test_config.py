import pathlib
import yaml

from pavo.utils import config


def test_get_config_value(monkeypatch, tmp_path) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        yaml,
        "load",
        lambda _, **kwargs: {"test": {"value": 10, "something": {"value": 11}}},
    )
    pathlib.Path(f"{tmp_path}/pavoconfig.yaml").touch()

    assert config.get_config_value("test.value") == 10
    assert config.get_config_value("test.something.value") == 11
    assert config.get_config_value("test.unexisting") == ""
    assert config.get_config_value("test.something") == {"value": 11}
