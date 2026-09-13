"""Shared test setup."""

import pytest

from pydsa import app, settings
from pydsa.settings import Settings
from pydsa.ui.console import console, force_colors_off


@pytest.fixture(autouse=True)
def fixed_console_width():
    """Render at a fixed width, so the layout doesn't depend on the terminal running the tests."""
    console.width = 100


@pytest.fixture(autouse=True)
def isolated_settings(monkeypatch, tmp_path):
    """Keep saved files in a temporary PyDSA home and start every test from the default settings and colors."""
    monkeypatch.setenv("PYDSA_HOME", str(tmp_path / "pydsa-home"))
    settings.current = Settings()
    force_colors_off(False)
    yield
    settings.current = Settings()
    force_colors_off(False)


@pytest.fixture
def play(monkeypatch, capsys):
    """Run the whole app with scripted answers and return everything it printed.

    An exception class among the answers, such as KeyboardInterrupt, is raised at that prompt instead.
    """

    def run_session(*answers, argv=()):
        remaining = iter(answers)

        def scripted_input(prompt=""):
            print(prompt, end="")
            try:
                answer = next(remaining)
            except StopIteration:
                raise AssertionError("The app asked for more input than the script provides") from None
            if isinstance(answer, type) and issubclass(answer, BaseException):
                raise answer
            return answer

        monkeypatch.setattr("builtins.input", scripted_input)
        app.run(list(argv))
        assert list(remaining) == [], "The app exited before using every scripted answer"
        return capsys.readouterr().out

    return run_session
