"""Bloom-filter bit choices, stable salted hashes and honest membership answers."""

from pydsa.content import texts
from pydsa.core.bloom_filter import BloomFilter
from pydsa.ui import random_data, render, stepper
from pydsa.ui.console import ask_int, ask_value, info, result, success
from pydsa.ui.menu import Menu, Nav, back_option, operation_menu


def run():
    render.intro(texts.BLOOM_FILTER_ASCII, "bloom-filter")
    bloom = Menu("🛠️ How do you want to create the Bloom filter?", [
        [("Create an empty filter", create), ("Use the example", example),
         ("Fill with random values", lambda: create(True))], [back_option()],
    ]).open()
    if bloom is Nav.BACK:
        return Nav.BACK
    return operation_menu("Bloom filter", "bloom-filter", operations(bloom), new_label="New Bloom Filter").run()


def create(random=False):
    m = ask_int("🔢 Number of bits m (1–512)?", "bit count", min_value=1, max_value=512)
    k = ask_int("🔢 Number of salted hashes k (1–10)?", "hash count", min_value=1, max_value=10)
    bloom = BloomFilter(m, k)
    if random:
        for word in random_data.words(random_data.ask_count("words")):
            bloom.add(word)
    success(f"Created a Bloom filter with {m} bits and {k} hashes.")
    render.bloom_filter(bloom)
    return bloom


def example():
    bloom = BloomFilter(32, 3)
    for word in ("apple", "pear", "plum"):
        bloom.add(word)
    success("Loaded the example Bloom filter with 32 bits and 3 hashes.")
    render.bloom_filter(bloom)
    return bloom


def operations(bloom):
    return [("Add", lambda: add(bloom)), ("Might Contain", lambda: check(bloom)),
            ("Display", lambda: render.bloom_filter(bloom))]


def add(bloom):
    word, trace = ask_value("str", "word"), []
    bloom.add(word, trace)
    stepper.play(trace, render.bloom_step)
    success(f"Added {render.fmt(word)} to the filter.")
    render.bloom_filter(bloom)


def check(bloom):
    word, trace = ask_value("str", "word"), []
    possible = bloom.might_contain(word, trace)
    stepper.play(trace, render.bloom_step)
    result(f"{render.fmt(word)}: {'might contain' if possible else 'definitely absent'}.")
    if possible:
        info("All checked bits are set, but other words can set the same bits. This may be a false positive; check the original data to be sure.")
    else:
        info("A checked bit is 0, so this word has not been added. Adding items never clears bits.")
