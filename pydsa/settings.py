"""User settings, saved as JSON in the PyDSA home folder so they last between sessions."""

import json
import os
from dataclasses import asdict, dataclass, fields
from pathlib import Path

VERSION = 1  # Bumped whenever the saved format changes

# The allowed values of every setting that isn't simply on or off
CHOICES = {
    "detail": ("brief", "detailed"),
    "steps": ("ask", "all", "pause"),
    "intro": ("once", "always"),
}


@dataclass(frozen=True)
class Settings:
    """How PyDSA behaves."""

    detail: str = "brief"  # How much of an algorithm's explanation to show before it runs
    steps: str = "ask"  # Whether operations with many steps pause after each one
    colors: bool = True
    clear_screen: bool = True  # Clear the terminal when opening a topic, starting it over or going home
    intro: str = "once"  # Show the full welcome intro once per session, or on every trip to the main menu


current = Settings()  # The settings in use for this session


def home():
    """Return the folder PyDSA saves its files in: PYDSA_HOME if it's set, otherwise ~/.pydsa."""
    folder = os.environ.get("PYDSA_HOME")
    return Path(folder) if folder else Path.home() / ".pydsa"


def path():
    """Return the path of the settings file."""
    return home() / "settings.json"


def _is_valid(name, value):
    if name in CHOICES:
        return value in CHOICES[name]
    return isinstance(value, bool)


def load():
    """Read the saved settings; return them and a notice if the file couldn't be fully used (None otherwise).

    A missing file quietly gives the defaults, and any value that's invalid falls back to its default.
    """
    file = path()
    try:
        data = json.loads(file.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return Settings(), None
    except (OSError, ValueError):
        return Settings(), f"Couldn't read the settings file ({file}), so the default settings are used."
    if not isinstance(data, dict):
        return Settings(), f"The settings file ({file}) isn't in the right format, so the default settings are used."

    values, invalid = {}, False
    for field in fields(Settings):
        if field.name in data:
            if _is_valid(field.name, data[field.name]):
                values[field.name] = data[field.name]
            else:
                invalid = True
    notice = "Some saved settings weren't valid, so their default values are used." if invalid else None
    return Settings(**values), notice


def load_current():
    """Make the saved settings the current ones; return a notice if the file couldn't be fully used."""
    global current
    current, notice = load()
    return notice


def save(new_settings):
    """Make new_settings current and save them; return a notice if they couldn't be saved (None otherwise)."""
    global current
    current = new_settings
    file = path()
    try:
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(json.dumps({"version": VERSION, **asdict(new_settings)}, indent=2) + "\n", encoding="utf-8")
    except OSError:
        return f"Couldn't save the settings to {file}, so they'll only last until you quit."
    return None
