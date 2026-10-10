"""String-search alignments, KMP prefix reuse and verified rolling-hash matches."""

import random

from pydsa.algorithms import string_search
from pydsa.content import texts
from pydsa.ui import render, stepper
from pydsa.ui.console import ask, ask_int, error, info, result
from pydsa.ui.menu import Menu, Nav, back_option, operation_menu
from pydsa.ui.screens.sorting_algorithms import Algorithm

SEARCHES = (
    Algorithm("Naive Search", string_search.naive_search, "naive-string-search"),
    Algorithm("KMP", string_search.kmp_search, "kmp"),
    Algorithm("Rabin-Karp", string_search.rabin_karp, "rabin-karp"),
)
MAX_TEXT, MAX_PATTERN = 80, 20
ART = {"naive-string-search": texts.NAIVE_STRING_SEARCH_ASCII,
       "kmp": texts.KMP_ASCII, "rabin-karp": texts.RABIN_KARP_ASCII}


def run():
    render.intro(texts.STRING_ALGORITHMS_ASCII, "string-algorithms")
    data = Menu("🛠️ How do you want to choose the text and pattern?", [
        [("Type text and pattern", create), ("Use the example", example),
         ("Generate random text and pattern", random_example)], [back_option()],
    ]).open()
    if data is Nav.BACK:
        return Nav.BACK
    return operation_menu("text and pattern", "string-algorithms", operations(*data),
                          guides=[search.guide for search in SEARCHES], new_label="New Text and Pattern").run()


def read_string(name, maximum):
    while True:
        value = ask(f"✍️ Enter the {name} (up to {maximum} characters; Enter means empty):")
        if len(value) <= maximum:
            return value  # Spaces are part of the input, including at either end.
        error(f"The {name} must have at most {maximum} characters.")


def create():
    data = read_string("text", MAX_TEXT), read_string("pattern", MAX_PATTERN)
    render.string_data(*data)
    return data


def example():
    data = "ABABABACABABAC", "ABABAC"
    info("Loaded a repeated-prefix example: try KMP to see why it reuses comparisons.")
    render.string_data(*data)
    return data


def random_example():
    n = ask_int("🎲 How many text characters (0–80)?", "text length", min_value=0, max_value=MAX_TEXT)
    m = ask_int("🎲 How many pattern characters (0–20)?", "pattern length", min_value=0, max_value=MAX_PATTERN)
    text = "".join(random.choice("ABCD") for _ in range(n))
    # A text slice often produces a match; longer patterns and empty inputs remain valid.
    if 0 < m <= n and random.choice((True, False)):
        start = random.randrange(n - m + 1)
        pattern = text[start:start + m]
    else:
        pattern = "".join(random.choice("ABCD") for _ in range(m))
    render.string_data(text, pattern)
    return text, pattern


def operations(text, pattern):
    return [*[(search.name, lambda search=search: search_text(text, pattern, search)) for search in SEARCHES],
            ("Compare Algorithms", lambda: compare(text, pattern)),
            ("Display", lambda: render.string_data(text, pattern))]


def ask_modulus():
    info("101 is the usual example modulus. Try 2 to make spurious hash hits easy to see; every hit is verified.")
    return ask_int("🔢 Hash modulus (2–1000003)?", "modulus", min_value=2, max_value=1_000_003)


def search_text(text, pattern, search):
    render.ascii_art(ART[search.guide])
    render.explanation(search.guide)
    options = {"modulus": ask_modulus()} if search.guide == "rabin-karp" else {}
    trace, stats = [], string_search.SearchStats()
    matches = search.function(text, pattern, trace, stats=stats, **options)

    def all_states(events):
        for number, event in enumerate(events, 1):
            render.string_step(number, event)

    stepper.play(trace, render.string_step, summary=all_states)
    result(f"Match positions: {matches}.")
    result(f"Character comparisons: {stats.comparisons} in search + {stats.preprocessing} in preprocessing = {stats.total} total.")
    if search.guide == "kmp":
        info(f"Prefix reuse avoided rechecking {stats.reused} known characters across shifts. Compare Algorithms shows the actual counts for this input.")
    if search.guide == "rabin-karp":
        info(f"Verified {stats.spurious_hits} spurious hash hits; hash arithmetic is separate from character comparisons.")


def compare(text, pattern):
    modulus = ask_modulus()
    rows = []
    for search in SEARCHES:
        stats = string_search.SearchStats()
        options = {"modulus": modulus} if search.guide == "rabin-karp" else {}
        matches = search.function(text, pattern, stats=stats, **options)
        rows.append((search.name, matches, stats))
    render.string_comparison(rows, modulus)
