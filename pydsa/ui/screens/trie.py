"""Trie (prefix tree) screen."""

from pydsa.content import texts
from pydsa.core.errors import DuplicateError, NotFoundError
from pydsa.core.trie import Trie
from pydsa.ui import random_data, render, stepper
from pydsa.ui.console import ask, error, info, not_found, plural, result, success, yes_no
from pydsa.ui.menu import Menu, Nav, back_option, operation_menu
from pydsa.ui.render import fmt

EXAMPLE_WORDS = ["car", "card", "care", "cat", "do", "dog"]


def run():
    """Create a trie and run the trie operation menu."""
    render.intro(texts.TRIE_ASCII, "trie")
    trie = Menu("🛠️ Do you want to start with an empty trie or use the preloaded example?", [
        [("Start with an empty trie", create), ("Use the example", example), ("Fill with random values", fill_random)],
        [back_option()],
    ]).open()
    if trie is Nav.BACK:
        return Nav.BACK

    return operation_menu("trie", "trie", operations(trie), new_label="New Trie").run()


def operations(trie):
    """Return the trie's operations as (label, action) pairs."""
    return [
        ("Insert a Word", lambda: insert(trie)),
        ("Delete a Word", lambda: delete(trie)),
        ("Search a Word", lambda: search(trie)),
        ("Prefix Check", lambda: prefix_check(trie)),
        ("Autocomplete", lambda: autocomplete(trie)),
        ("Word Count", lambda: word_count(trie)),
        ("Display", lambda: render.trie(trie)),
    ]


def create():
    success("Created an empty trie.")
    return Trie()


def example():
    """Return the preloaded example trie."""
    trie = Trie(EXAMPLE_WORDS)
    words = ", ".join(fmt(word) for word in EXAMPLE_WORDS[:-1])
    success(f"Loaded the example trie with the words {words} and {fmt(EXAMPLE_WORDS[-1])}.")
    render.trie(trie)
    return trie


def fill_random():
    """Ask how many random words to insert and return the trie."""
    count = random_data.ask_count("words", maximum=len(random_data.TRIE_WORDS))
    trie = Trie(random_data.trie_words(count))
    success(f"Created a trie with {plural(count, 'random word')}.")
    render.trie(trie)
    return trie


def ask_word():
    """Ask until a word with at least one character is typed; spaces around it are dropped."""
    while True:
        word = ask("✍️ Enter the word:").strip()
        if word:
            return word
        error("The word needs at least one character.")


def ask_prefix():
    return ask("✍️ Enter the prefix (leave it empty to match every word):").strip()


def show_steps(trace):
    """Play the steps of a trie operation, drawing the path spelled out so far after each one."""
    stepper.play(trace, render.prefix_step)


def insert(trie):
    word = ask_word()
    trace = []
    try:
        added = trie.insert(word, trace)
    except DuplicateError:
        info(f"{fmt(word)} is already in the trie, so nothing changed.")
        return
    show_steps(trace)
    success(f"Inserted {fmt(word)} with {plural(added, 'new node')}.")
    if added < len(word):
        info(f"The first {plural(len(word) - added, 'character')} reused nodes that other words already had.")
    render.trie(trie)


def delete(trie):
    word = ask_word()
    trace = []
    try:
        pruned = trie.delete(word, trace)
    except NotFoundError:
        not_found(f"{fmt(word)} isn't in the trie, so nothing was deleted.")
        return
    show_steps(trace)
    if pruned:
        success(f"Deleted {fmt(word)} and pruned {plural(pruned, 'node')} that no longer led to a word.")
    else:
        success(f"Deleted {fmt(word)}. Other words still use all of its nodes, so only its word mark was removed.")
    render.trie(trie)


def search(trie):
    word = ask_word()
    trace = []
    found = trie.search(word, trace)
    show_steps(trace)
    if found:
        success(f"Found {fmt(word)} in the trie.")
    elif trie.starts_with(word):
        not_found(f"{fmt(word)} isn't a word in the trie, although some words start with it.")
    else:
        not_found(f"{fmt(word)} isn't in the trie.")


def prefix_check(trie):
    prefix = ask_prefix()
    result(f"Does any word start with {fmt(prefix)}? {yes_no(trie.starts_with(prefix))}.")


def autocomplete(trie):
    prefix = ask_prefix()
    words = trie.autocomplete(prefix)
    if words:
        result(f"Words starting with {fmt(prefix)}: {', '.join(fmt(word) for word in words)}")
    else:
        not_found(f"No words start with {fmt(prefix)}.")


def word_count(trie):
    result(f"The trie holds {plural(len(trie), 'word')} in {plural(trie.node_count(), 'node')}, not counting the root.")
