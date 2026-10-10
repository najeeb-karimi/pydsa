"""Cache and probabilistic-topic screens, practice, diagrams and growth experiments."""

import random

import pytest
from rich.cells import cell_len

from pydsa import progress, settings
from pydsa.content import notes, texts
from pydsa.core.bloom_filter import BloomFilter
from pydsa.core.lru_cache import LRUCache
from pydsa.core.skip_list import SkipList
from pydsa.practice import challenges, experiments
from pydsa.ui import render, stepper
from pydsa.ui.console import console


TOPICS = ("lru-cache", "skip-list", "bloom-filter")


def test_cache_all_operations_eviction_code_restart_home(play):
    out = play("2", "1", "2", "1", "A", "3", "1", "D", "2", "40",
               "2", "1", "B", "3", "1", "A", "2", "99", "4",
               "5", "1", "5", "2", "6", "2", "7", "0", argv=["--topic", "lru-cache"])
    assert "What it is" in out and "Get 'A': 10." in out
    assert "Evicted least recent key 'B'" in out and "'B' is not cached" in out
    assert "Pseudocode: Get" in out and "Pseudocode: Put" in out and "def put(" in out
    assert "Goodbye!" in out and "lru-cache" in progress.current.visited


def test_skip_all_operations_coin_flips_duplicates_code_restart_home(play):
    out = play("2", "1", "2", "1", "25", "2", "1", "25", "3", "1", "25",
               "4", "1", "25", "4", "1", "999", "3", "1", "999", "5",
               "6", "1", "6", "2", "6", "3", "7", "2", "8", "0", argv=["--topic", "skip-list"])
    assert "seed 7" in out and "seeded coin" in out and "level" in out and "moved right" in out
    assert "Inserted 25." in out and "Deleted one occurrence of 25." in out
    assert "Found 25" in out and "999 is not in the skip list" in out
    assert all(f"Pseudocode: {operation}" in out for operation in ("Insert", "Delete", "Search"))
    assert "Goodbye!" in out


def test_bloom_all_operations_absence_code_restart_home(play):
    out = play("2", "1", "2", "kiwi", "3", "kiwi", "3", "not-added", "4",
               "5", "1", "5", "2", "6", "2", "7", "0", argv=["--topic", "bloom-filter"])
    assert "Added 'kiwi'" in out and "'kiwi': might contain" in out
    assert "definitely absent" in out and "false positive" in out and "Salted hash" in out
    assert "Pseudocode: Add" in out and "Pseudocode: Might Contain" in out and "def positions(" in out
    assert "Goodbye!" in out


def test_tiny_bloom_explains_false_positive_and_hash_limits(play):
    out = play("1", "0", "513", "1", "0", "11", "3", "2", "apple", "3", "never added", "0",
               argv=["--topic", "bloom-filter"])
    assert "must be at least 1" in out and "must be at most 512" in out and "must be at most 10" in out
    assert "'never added': might contain" in out and "This may be a false positive" in out


def test_cache_capacity_one_and_invalid_numeric_keys(play):
    out = play("1", "0", "51", "1", "3", "1", "key", "2", "1", "3", "3", "nan", "2", "2",
               "2", "3", "inf", "3", "1", "new", "2", "2", "2", "1", "new", "0",
               argv=["--topic", "lru-cache"])
    assert "must be at most 50" in out and "Numeric cache keys must be finite" in out
    assert "Evicted least recent key 'key'" in out and "Get 'new': 2." in out


def test_skip_word_keys_seed_and_invalid_number(play):
    out = play("1", "2", "no", "5", "2", "pear", "2", "apple", "2", "pear", "3", "pear",
               "4", "pear", "7", "1", "1", "9", "2", "2", "nan", "0", argv=["--topic", "skip-list"])
    assert "seed must be a whole number" in out and "Found 'pear'" in out
    assert "finite num values" in out and "Seed 9" in out


@pytest.mark.parametrize("topic,answers", [
    ("lru-cache", ["3", "4", "3", "0"]),
    ("skip-list", ["3", "1", "42", "8", "0"]),
    ("skip-list", ["3", "2", "42", "8", "0"]),
    ("bloom-filter", ["3", "64", "3", "8", "0"]),
])
def test_random_creation(play, topic, answers):
    out = play(*answers, argv=["--topic", topic])
    assert "Created" in out and "Goodbye!" in out
    if topic == "skip-list":
        assert "seeded coin" in out and "Seed 42" in out


@pytest.mark.parametrize("topic", TOPICS)
@pytest.mark.parametrize("interrupt", [KeyboardInterrupt, EOFError, ":b"])
def test_interrupted_creation_is_clean(play, topic, interrupt):
    setup = ["1", "1"] if topic == "skip-list" else ["1"]
    tail = ["0", "0"] if interrupt == ":b" else []
    out = play(*setup, interrupt, *tail, argv=["--topic", topic])
    assert "Goodbye!" in out and "Traceback" not in out


@pytest.mark.parametrize("topic", TOPICS)
def test_cancelled_operations_return_to_menu(play, topic):
    if topic == "lru-cache":
        answers = ["2", "3", "1", ":b", "2", "1", "A", "0"]
    elif topic == "skip-list":
        answers = ["2", "2", "1", ":b", "4", "1", "10", "0"]
    else:
        answers = ["2", "2", ":b", "3", "apple", "0"]
    out = play(*answers, argv=["--topic", topic])
    assert "Cancelled." in out and "Goodbye!" in out


def test_new_category_routes(play):
    out = play("1", "6", "2", "0")
    assert "skip list" in out and "Goodbye!" in out
    out = play("4", "3", "2", "0")
    assert "Bloom-filter bits" in out and "Goodbye!" in out
    out = play("4", "4", "2", "0")
    assert "Key table" in out and "Goodbye!" in out


@pytest.mark.parametrize("topic", TOPICS)
def test_practice_quizzes_predictions_and_experiments(play, monkeypatch, topic):
    monkeypatch.setattr(random.Random, "shuffle", lambda self, items: None)
    challenge = challenges.make(topic, random.Random(6))
    monkeypatch.setattr(challenges, "make", lambda topic_id: challenge)
    practice = "9" if topic == "skip-list" else "8"
    exp = ["3"] if topic == "lru-cache" else ["3", "1", "2", "0"]
    out = play("2", practice, "1", "a", "a", "a", "a", "a", "2", repr(challenge.answer),
               *exp, "0", "0", argv=["--topic", topic])
    assert "Quiz score: 5/5" in out and "Correct prediction" in out
    if topic == "bloom-filter":
        assert "Measured" in out and "Formula" in out
    elif topic == "skip-list":
        assert "Ratio" in out
    assert progress.current.quizzes[topic].best == 100 and progress.current.challenges[topic] == 1


@pytest.mark.parametrize("width", [45, 90])
@pytest.mark.parametrize("topic", TOPICS)
def test_all_views_and_paused_states_fit_without_color(play, monkeypatch, capsys, width, topic):
    console.width = width
    monkeypatch.setattr(render, "ascii_art", lambda art: None)
    monkeypatch.setattr(stepper, "can_pause", lambda: True)
    settings.save(settings.Settings(steps="pause", colors=False))
    if topic == "lru-cache":
        answers = ["2", "1", "2", "1", "A", "a", "3", "1", "D", "2", "40", "a", "5", "2", "0"]
    elif topic == "skip-list":
        answers = ["2", "1", "2", "1", "25", "a", "4", "1", "50", "a", "3", "1", "25", "a", "6", "1", "0"]
    else:
        answers = ["2", "1", "2", "kiwi", "a", "3", "kiwi", "a", "5", "1", "0"]
    out = play(*answers, argv=["--topic", topic, "--no-color"])
    assert "Step 1:" in out and "*" in out and "\x1b[" not in out
    assert all(cell_len(line) <= width for line in out.splitlines())
    # Long data forces the compact layouts and must never overflow a narrow terminal.
    if topic == "lru-cache":
        structure = LRUCache(12)
        for i in range(12):
            structure.put(f"very-long-key-[{i}]", f"very-long-value-{i}")
        render.lru_cache(structure)
    elif topic == "skip-list":
        structure = SkipList("str", seed=8)
        for i in range(30):
            structure.insert(f"long-key-[{i:02d}]")
        render.skip_list(structure)
    else:
        structure = BloomFilter(512, 10)
        structure.add("word")
        render.bloom_filter(structure)
    for note in notes.NOTES:
        if note.topic == topic and note.sources:
            render.code(note)
    out = capsys.readouterr().out
    assert all(cell_len(line) <= width for line in out.splitlines())
    if topic == "skip-list":
        assert "too wide to align" in out


@pytest.mark.parametrize("topic", TOPICS)
def test_paused_steps_can_stop(play, monkeypatch, topic):
    monkeypatch.setattr(stepper, "can_pause", lambda: True)
    settings.save(settings.Settings(steps="pause"))
    choices = ["2", "2", "1", "A", "s", "0"] if topic == "lru-cache" else (
        ["2", "2", "1", "25", "s", "0"] if topic == "skip-list" else ["2", "2", "kiwi", "s", "0"])
    out = play(*choices, argv=["--topic", topic])
    assert "Stopped after" in out and "Goodbye!" in out


def test_bloom_experiment_uses_absent_queries_and_compares_with_formula():
    experiment, = experiments.for_topic("bloom-filter")
    for mode in experiments.MODES:
        rows = experiments.measure(experiment, mode, rng=random.Random(14))
        assert all(0 <= row.false_positives <= row.trials == 2000 for row in rows)
        assert all(row.measured == row.false_positives / row.trials for row in rows)
        assert all(abs(row.measured - row.expected) < 0.04 for row in rows)
        assert rows[-1].measured > rows[0].measured
        bloom, queries = experiment.make_input(128, mode, random.Random(8))
        assert len(set(queries)) == 2000 and all(item.startswith("absent:") for item in queries)
        assert all(bloom.might_contain(f"added:{i}") for i in range(128))
        assert experiment.run((bloom, queries)) == sum(bloom.might_contain(item) for item in queries)


def test_skip_search_experiment_has_seeded_short_paths():
    experiment, = experiments.for_topic("skip-list")
    for mode in experiments.MODES:
        rows = experiments.measure(experiment, mode, rng=random.Random(12))
        assert all(0 < row.work < 5 * experiments.LOG(row.n) for row in rows)


def test_ascii_titles():
    assert all(len(art.splitlines()) >= 9 for art in (texts.LRU_CACHE_ASCII, texts.SKIP_LIST_ASCII, texts.BLOOM_FILTER_ASCII))
