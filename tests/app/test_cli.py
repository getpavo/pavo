import pytest

from pavo.app import PavoApp
from pavo.utils import files, config


def test_discover_plugins():
    app = PavoApp()
    assert app.discover_plugins() is None


def test_run_incorrect_version(monkeypatch, capsys):
    app = PavoApp()
    monkeypatch.setattr(app, "has_correct_version", lambda: False)

    with pytest.raises(SystemExit):
        app.run()

    captured = capsys.readouterr()
    assert (
        "Your Pavo config file version does not match your Pavo version."
        in captured.out
    )


def test_run_no_args_shows_help(capsys):
    app = PavoApp()

    with pytest.raises(SystemExit):
        app.run()

    captured = capsys.readouterr()
    assert "Showing help for all 4 Pavo commands:" in captured.out


def test_run_help(capsys):
    app = PavoApp()

    with pytest.raises(SystemExit):
        app.run(["help"])

    captured = capsys.readouterr()
    assert "Showing help for all 4 Pavo commands:" in captured.out


def test_handles_error_when_running(monkeypatch, capsys):
    app = PavoApp()
    default_error_message = "Something went wrong, check the logs for more info"
    test_message_value = "This is a test value"

    # Test if we get the default message when the error thrown has no custom message
    monkeypatch.setattr(
        app.command_manager,
        "execute",
        lambda _first, _second: (_ for _ in ()).throw(ValueError()),
    )

    with pytest.raises(SystemExit):
        app.run(["help"])

    captured = capsys.readouterr()
    assert default_error_message in captured.out

    # When an error message is set, we should also see it in the output, instead of the default message
    monkeypatch.setattr(
        app.command_manager,
        "execute",
        lambda _first, _second: (_ for _ in ()).throw(ValueError(test_message_value)),
    )

    with pytest.raises(SystemExit):
        app.run(["help"])

    captured = capsys.readouterr()
    assert test_message_value in captured.out
    assert default_error_message not in captured.out


def test_has_correct_version(monkeypatch, capsys):
    app = PavoApp()

    # Test if we get True when we are not in a project
    monkeypatch.setattr(files, "cd_is_project", lambda: False)
    assert app.has_correct_version() is True

    # We must mock that we are now in a project
    monkeypatch.setattr(files, "cd_is_project", lambda: True)

    # Test if we get True if the version matches
    monkeypatch.setattr(config, "get_config_value", lambda _: "1.0-test")
    monkeypatch.setattr(app, "version", "1.0-test")
    assert app.has_correct_version() is True

    # Test if we get False if the version does not match
    monkeypatch.setattr(app, "version", "1.1-test")
    assert app.has_correct_version() is False
