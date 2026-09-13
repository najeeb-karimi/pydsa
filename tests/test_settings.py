"""Loading and saving settings, including missing, corrupt and unwritable files."""

import json
from pathlib import Path

from pydsa import settings
from pydsa.settings import Settings


def test_defaults_when_nothing_is_saved():
    assert settings.load() == (Settings(), None)


def test_save_and_load_round_trip():
    chosen = Settings(detail="detailed", steps="pause", colors=False, clear_screen=False, intro="always")
    assert settings.save(chosen) is None
    assert settings.current == chosen
    assert json.loads(settings.path().read_text(encoding="utf-8"))["version"] == settings.VERSION
    assert settings.load() == (chosen, None)


def test_corrupt_file_gives_the_defaults():
    settings.path().parent.mkdir(parents=True)
    settings.path().write_text("{not json", encoding="utf-8")
    loaded, notice = settings.load()
    assert loaded == Settings()
    assert "Couldn't read the settings file" in notice


def test_wrong_shape_and_invalid_values():
    settings.path().parent.mkdir(parents=True)
    settings.path().write_text("[1, 2]", encoding="utf-8")
    loaded, notice = settings.load()
    assert loaded == Settings() and "isn't in the right format" in notice

    settings.path().write_text(json.dumps({"detail": "loud", "colors": "yes", "intro": "always", "extra": 1}), encoding="utf-8")
    loaded, notice = settings.load()
    assert loaded == Settings(intro="always")  # The valid value is kept, the invalid ones fall back
    assert "weren't valid" in notice


def test_unreadable_file():
    settings.path().mkdir(parents=True)  # A folder where the file should be
    loaded, notice = settings.load()
    assert loaded == Settings() and "Couldn't read" in notice


def test_unwritable_home_keeps_the_settings_for_the_session(monkeypatch, tmp_path):
    blocker = tmp_path / "file"
    blocker.write_text("", encoding="utf-8")
    monkeypatch.setenv("PYDSA_HOME", str(blocker))
    notice = settings.save(Settings(detail="detailed"))
    assert "Couldn't save the settings" in notice
    assert settings.current.detail == "detailed"


def test_home_defaults_to_the_user_folder(monkeypatch):
    monkeypatch.delenv("PYDSA_HOME")
    assert settings.home() == Path.home() / ".pydsa"
