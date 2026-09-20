"""The step player: shows the steps of an operation one at a time, or all of them at once.

An operation hands its TraceEvents to play(), together with a way to draw one step. What happens then
follows the Steps setting: "all" never stops, "pause" waits after every step, and "ask" asks first.
Steps are only ever played in a real terminal, so a scripted or piped run simply reads on.
"""

import sys

from rich.text import Text

from pydsa import settings
from pydsa.ui import render
from pydsa.ui.console import PROMPT, BackRequested, QuitRequested, ask, console, info

MANY_STEPS = 200  # More steps than anyone wants to walk through one at a time


def can_pause():
    """Return True when a pause can be answered: a real terminal whose input is typed live."""
    return console.is_terminal and sys.stdin.isatty()


def play(events, draw, summary=None, label=render.fmt):
    """Show the steps of an operation and return them as a list.

    draw(number, event) draws one step with the state it left behind. summary(events) shows every step in a
    short form, such as a table; without one, the steps are listed as sentences. At a pause, Enter shows the
    next step, a shows the rest and s stops.
    """
    events = list(events)
    if not events:
        return events
    if _watch(len(events)):
        _one_at_a_time(events, draw)
    elif summary is not None:
        summary(events)
    else:
        render.step_captions(events, label)
    return events


def _watch(count):
    """Return True if the steps should be shown one at a time, asking the user when the setting says so."""
    if count < 2 or not can_pause() or settings.current.steps == "all":
        return False
    try:
        if count > MANY_STEPS:
            info(f"This run takes {count} steps, which is a lot to watch one at a time.")
            return _yes(f"👀 Watch all {count} steps anyway? Press Enter for the short version, or type y:")
        if settings.current.steps == "pause":
            return True
        return _yes("👀 Watch it step by step? Press Enter to see it all at once, or type y:")
    except BackRequested:
        return False  # The work is done either way, so cancelling only skips the steps


def _yes(question):
    return ask(question).strip().lower() in ("y", "yes")


def _one_at_a_time(events, draw):
    """Draw one step after another, waiting for the user in between."""
    total = len(events)
    for number, event in enumerate(events, start=1):
        draw(number, event)
        if number == total:
            return
        console.print(Text(f"Step {number} of {total} · Enter: next · a: the rest · s: stop", style="muted"))
        answer = input(PROMPT).strip().lower()
        if answer == ":q":
            raise QuitRequested
        if answer in ("s", "q", "b", ":b"):
            info(f"Stopped after {number} of {total} steps.")
            return
        if answer == "a":
            for rest, later in enumerate(events[number:], start=number + 1):
                draw(rest, later)
            return
