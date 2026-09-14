"""Learning Tools screen: the overview, every guide, the glossary and help choosing a data structure."""

import difflib

from pydsa import topics
from pydsa.content import registry
from pydsa.ui import render
from pydsa.ui.console import ask, error, not_found, plural, result
from pydsa.ui.menu import Menu, Nav, back_option


def run():
    """Keep offering the learning tools until the user goes back to the main menu."""
    menu = Menu("🧰 Which learning tool do you want to use?", [
        [("Overview", lambda: render.document("overview", "🏗️")),
         ("Browse the Guides", browse),
         ("Glossary", glossary),
         ("Which Data Structure Should I Use?", lambda: render.document("choosing", "🧭"))],
        [back_option()],
    ])
    while True:
        if menu.select() is Nav.BACK:
            return None  # Not Nav.BACK, which would end the main menu


def browse():
    """Let the user pick a category, then read its guides, until they go back."""
    menu = Menu("📚 Which guides do you want to browse?", [
        [(title, lambda category=category: pick_guide(category)) for category, title in topics.CATEGORIES.items()],
        [back_option()],
    ])
    while menu.select() is not Nav.BACK:
        pass


def pick_guide(category):
    """Let the user read the guides of one category, sub-topics included, until they go back."""
    menu = Menu("📖 Which guide do you want to read?", [
        [(topic.title if topic.parent is None else f"↳ {topic.title}", lambda topic=topic: render.guide(topic.id))
         for topic in topics.TOPICS if topic.category == category],
        [back_option()],
    ], compact_repeat=True)
    while menu.select() is not Nav.BACK:
        pass


def glossary():
    """List every glossary term or look terms up, until the user goes back."""
    menu = Menu("📘 What do you want to do in the glossary?", [
        [(f"List All {len(registry.glossary())} Terms, A to Z", lambda: render.glossary(registry.glossary())),
         ("Look Up a Term", look_up)],
        [back_option()],
    ])
    while menu.select() is not Nav.BACK:
        pass


def look_up():
    """Ask for part of a term and show every term that contains it, or suggest the closest ones."""
    query = ask("🔎 Type a term, or part of one (such as amort):").strip()
    if not query:
        error("Type at least one letter to look up.")
        return
    terms = registry.find_terms(query)
    if terms:
        result(f"Found {plural(len(terms), 'term')} matching {query!r}.")
        render.glossary(terms)
        return
    # Compare with the plain names, without "(...)" parts, so "vertx" still finds "Vertex (plural: vertices)"
    names = {term.slug.replace("-", " "): term.name for term in registry.glossary()}
    close = [names[match] for match in difflib.get_close_matches(query.casefold(), names, n=3, cutoff=0.6)]
    hint = f" Did you mean {' or '.join(close)}?" if close else " Choose List All Terms to see every term."
    not_found(f"No term matches {query!r}.{hint}")
