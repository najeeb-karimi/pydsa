"""Settings screen: change how PyDSA behaves. Every change is saved right away."""

from dataclasses import replace

from pydsa import settings
from pydsa.settings import Settings
from pydsa.ui.console import apply_colors, colors_forced_off, error, info, success
from pydsa.ui.menu import Menu, Nav, back_option

DETAIL = {"brief": "Brief", "detailed": "Detailed"}
INTRO = {"once": "Once per Session", "always": "Every Time"}


def on_off(value):
    return "On" if value else "Off"


def run():
    """Keep offering the settings until the user goes back to the main menu."""
    while True:
        current = settings.current
        choice = Menu("⚙️ Which setting do you want to change?", [
            [(f"Explanations: {DETAIL[current.detail]}", change_detail),
             (f"Colors: {on_off(current.colors)}", change_colors),
             (f"Clear the Screen: {on_off(current.clear_screen)}", change_clear_screen),
             (f"Welcome Intro: {INTRO[current.intro]}", change_intro)],
            [("Restore the Defaults", restore_defaults)],
            [back_option()],
        ]).select()
        if choice is Nav.BACK:
            return None  # Not Nav.BACK, which would end the main menu


def save(new_settings):
    """Make new_settings current, save them and report how that went."""
    problem = settings.save(new_settings)
    apply_colors()
    if problem:
        error(problem)
    else:
        success("Saved your settings.")


def pick(field, explanation, question, choices):
    """Explain a setting, then let the user pick one of choices, as (value, label) pairs, and save it."""
    info(explanation)
    current_value = getattr(settings.current, field)
    value = Menu(question, [
        [(f"{label} (current)" if value == current_value else label, lambda value=value: value) for value, label in choices],
        [back_option()],
    ]).select()
    if value is not Nav.BACK:
        save(replace(settings.current, **{field: value}))


def change_detail():
    pick("detail",
         "An explanation appears before an algorithm runs. Brief shows a short summary so you can get going "
         "quickly, and Detailed shows how the algorithm works, step by step. Either way, Read the Guide in a "
         "topic's menu shows the whole guide.",
         "📖 How much of each explanation do you want to see?",
         [("brief", "Brief"), ("detailed", "Detailed")])


def change_colors():
    pick("colors",
         "Colors highlight results, errors and the values that changed. Turn them off if your terminal shows "
         "strange symbols or you prefer plain text; marks like * then point out the changes instead.",
         "🎨 Should PyDSA use colors?",
         [(True, "On"), (False, "Off")])
    if settings.current.colors and colors_forced_off():
        info("Colors stay off for now, because PyDSA was started with --no-color or NO_COLOR is set.")


def change_clear_screen():
    pick("clear_screen",
         "When this is on, PyDSA clears the terminal when you open a topic, start it over or return to the main "
         "menu. Turn it off to keep everything you did on screen, so you can scroll back through it.",
         "🧹 Should PyDSA clear the screen?",
         [(True, "On"), (False, "Off")])


def change_intro():
    pick("intro",
         "The welcome intro shows the version, what's new and an overview of data structures and algorithms. It "
         "can show once per session, with a short header after that, or every time you return to the main menu.",
         "👋 When should the welcome intro show?",
         [("once", "Once per session"), ("always", "Every time I return to the main menu")])


def restore_defaults():
    confirmed = Menu("♻️ Do you want to restore every setting to its default?", [
        [("Yes, restore the defaults", lambda: True)],
        [back_option("No, keep my settings")],
    ]).select()
    if confirmed is True:
        save(Settings())
