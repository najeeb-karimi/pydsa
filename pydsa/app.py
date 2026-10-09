"""PyDSA entry point: reads the command-line options, then runs the main menu until the user exits."""

import argparse
import difflib

from pydsa import __version__, progress, settings, topics
from pydsa.settings import Settings
from pydsa.ui import render
from pydsa.ui.console import BackRequested, QuitRequested, clear, configure_output, console, force_colors_off, info, success
from pydsa.ui.menu import Menu, Nav, back_option, exit_option
from pydsa.ui.screens import settings as settings_screen
from pydsa.ui.screens import tools

QUESTIONS = {
    "linear": "🏁 Which linear data structure do you want to learn?",
    "non-linear": "🧭 Which non-linear data structure do you want to learn?",
    "algorithms": "🧮 Which algorithms do you want to learn?",
}


def parse_args(argv=None):
    """Parse the command-line options; exit with a helpful message for an unknown topic."""
    parser = argparse.ArgumentParser(prog="pydsa", description="Learn data structures and algorithms in your terminal.")
    parser.add_argument("--version", action="version", version=f"PyDSA {__version__}")
    parser.add_argument("--no-color", action="store_true", help="turn colors off for this run")
    parser.add_argument("--list-topics", action="store_true", help="show the ID of every topic and exit")
    parser.add_argument("--topic", metavar="ID", help="open a topic directly, such as stack or avl-tree")
    parser.add_argument("--reset-settings", action="store_true", help="restore the default settings before starting")
    args = parser.parse_args(argv)
    if args.topic is not None and topics.find(args.topic) is None:
        matches = difflib.get_close_matches(args.topic.lower(), [topic.id for topic in topics.TOPICS], n=3)
        hint = f" Did you mean {' or '.join(matches)}?" if matches else ""
        parser.error(f"unknown topic {args.topic!r}.{hint} Run pydsa --list-topics to see every topic.")
    return args


def open_topic(topic):
    """Open a topic, starting it again for as long as it returns Nav.NEW; return the Nav it ends with."""
    while True:
        clear()
        try:
            nav = topic.open()
        except BackRequested:
            return Nav.BACK
        if nav is not Nav.NEW:
            return nav


def pick_topic(category):
    """Let the user open topics from one category; return Nav.EXIT if they quit the program."""
    def open_from_list(topic):
        nav = open_topic(topic)
        return None if nav is Nav.BACK else nav

    while True:
        menu = Menu(QUESTIONS[category], [
            [(("✓ " if topic.id in progress.current.visited else "") + topic.title,
              lambda topic=topic: open_from_list(topic)) for topic in topics.listed(category)],
            [back_option()],
        ])
        nav = menu.select()
        if nav is Nav.EXIT:
            return Nav.EXIT
        if nav in (Nav.BACK, Nav.HOME):
            return None


def main_menu():
    from pydsa.ui.screens import practice
    return Menu("📂 What do you want to learn?", [
        [(title, lambda category=category: pick_topic(category)) for category, title in topics.CATEGORIES.items()],
        [("Learning Tools", tools.run), ("Settings", settings_screen.run), ("Practice", practice.run)],
        [exit_option()],
    ], can_go_back=False, status=render.progress_summary)


def run(argv=None):
    """Read the options, then show the intro and keep offering the main menu until the user exits.

    Ctrl+C, Ctrl+D and the quit shortcut all end the program with the usual goodbye.
    """
    configure_output()
    args = parse_args(argv)
    notice = settings.load_current()
    progress_notice = progress.load_current()
    if args.reset_settings:
        notice = settings.save(Settings())
    force_colors_off(args.no_color)
    if args.list_topics:
        render.topic_list(topics.TOPICS, topics.CATEGORIES)
        return

    render.start_session()
    try:
        start(args, notice, progress_notice)
    except (KeyboardInterrupt, EOFError, QuitRequested):
        console.print()
    render.goodbye()


def start(args, notice, progress_notice=None):
    """Show the intro or the requested topic, then the main menu."""
    if args.topic is None:
        render.home()
    else:
        render.skip_intro()
    if notice:
        info(notice)
    elif args.reset_settings:
        success("Restored the default settings.")
    if progress_notice:
        info(progress_notice)

    if args.topic is not None:
        nav = open_topic(topics.find(args.topic))
        if nav is Nav.EXIT:
            return
        if nav is not Nav.HOME:  # Main Menu already showed the header
            render.home()
    main_menu().run()
