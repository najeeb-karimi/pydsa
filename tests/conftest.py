"""Shared test setup."""

import pytest

from pydsa.ui.console import console


@pytest.fixture(autouse=True)
def fixed_console_width():
    """Render at a fixed width, so the layout doesn't depend on the terminal running the tests."""
    console.width = 100
