"""LRU cache creation, key-value operations and recency diagrams."""

from pydsa.content import texts
from pydsa.core.errors import InvalidTypeError, NotFoundError
from pydsa.core.lru_cache import LRUCache
from pydsa.ui import random_data, render, stepper
from pydsa.ui.console import ask_int, ask_value, error, not_found, result, success
from pydsa.ui.menu import Menu, Nav, back_option, operation_menu


def run():
    render.intro(texts.LRU_CACHE_ASCII, "lru-cache")
    cache = Menu("🛠️ How do you want to create the LRU cache?", [
        [("Create an empty cache", create), ("Use the example", example),
         ("Fill with random values", lambda: create(True))], [back_option()],
    ]).open()
    if cache is Nav.BACK:
        return Nav.BACK
    return operation_menu("LRU cache", "lru-cache", operations(cache), new_label="New LRU Cache").run()


def create(random=False):
    capacity = ask_int("🔢 How many entries can the cache hold (1–50)?", "capacity", min_value=1, max_value=50)
    cache = LRUCache(capacity)
    if random:
        count = random_data.ask_count("entries", maximum=capacity)
        for key, value in random_data.key_value_pairs(count):
            cache.put(key, value)
    success(f"Created the LRU cache with capacity {capacity}.")
    render.lru_cache(cache)
    return cache


def example():
    cache = LRUCache(3)
    for key, value in (("A", 10), ("B", 20), ("C", 30)):
        cache.put(key, value)
    success("Loaded the example LRU cache with capacity 3.")
    render.lru_cache(cache)
    return cache


def operations(cache):
    return [("Get", lambda: get(cache)), ("Put", lambda: put(cache)), ("Display", lambda: render.lru_cache(cache))]


def get(cache):
    key, trace = ask_value(what="key"), []
    try:
        value = cache.get(key, trace)
    except InvalidTypeError as problem:
        error(str(problem))
        return
    except NotFoundError:
        stepper.play(trace, render.lru_step)
        not_found(f"Key {render.fmt(key)} is not cached; its order stays unchanged.")
        return
    stepper.play(trace, render.lru_step)
    result(f"Get {render.fmt(key)}: {render.fmt(value)}.")
    render.lru_cache(cache)


def put(cache):
    key, value = ask_value(what="key"), ask_value(what="value")
    trace = []
    try:
        evicted = cache.put(key, value, trace)
    except InvalidTypeError as problem:
        error(str(problem))
        return
    stepper.play(trace, render.lru_step)
    success(f"Stored {render.fmt(key)}: {render.fmt(value)} as most recent.")
    if evicted is not None:
        result(f"Evicted least recent key {render.fmt(evicted[0])} with value {render.fmt(evicted[1])}.")
    render.lru_cache(cache)
