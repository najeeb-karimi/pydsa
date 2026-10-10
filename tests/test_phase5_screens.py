"""String-search menus, visible shifts and collisions, practice, size caps and plain narrow output."""

import random

import pytest
from rich.cells import cell_len

from pydsa import progress, settings
from pydsa.algorithms import string_search
from pydsa.content import notes, texts
from pydsa.practice import challenges, experiments
from pydsa.ui import render, stepper
from pydsa.ui.console import console

TOPICS = ("string-algorithms", "naive-string-search", "kmp", "rabin-karp")


def test_example_all_algorithms_guides_code_restart_and_home(play):
    out = play("2", "1", "1", "1", "2", "1", "3", "1", "4", "2", "3", "4", "2", "5", "101", "6",
               "7", "1", "7", "2", "7", "3", "7", "4", "8", "2", "9", "0",
               argv=["--topic", "string-algorithms"])
    assert "Match positions: [2, 8]." in out and "KMP prefix table" in out
    assert "known prefix characters" in out and "spurious" in out
    assert "Character comparisons" in out and "Search" in out and "Prefix" in out
    assert all(f"Pseudocode: {label}" in out for label in ("Naive Search", "KMP", "Rabin-Karp", "Compare Algorithms"))
    assert set(TOPICS) <= progress.current.visited.keys() and "Goodbye!" in out


def test_algorithm_category_route(play):
    out = play("5", "4", "2", "0")
    assert "Loaded a repeated-prefix example" in out and "Goodbye!" in out


def test_typed_whitespace_and_overlapping_results(play):
    out = play("1", " a a ", " a ", "2", "3", "4", "101", "5", "101", "0",
               argv=["--topic", "string-algorithms"])
    assert out.count("Match positions: [0, 2].") == 3
    assert "Text length: 5; pattern length: 3." in out and "·" in out


@pytest.mark.parametrize("text,pattern,answer", [("", "", "[0]"), ("abc", "", "[0, 1, 2, 3]"),
                                              ("", "abc", "[]"), ("a", "abc", "[]"),
                                              ("🦄é🦄é", "🦄é", "[0, 2]")])
def test_empty_longer_and_unicode_strings(play, text, pattern, answer):
    out = play("1", text, pattern, "2", "3", "4", "2", "5", "2", "0",
               argv=["--topic", "string-algorithms"])
    assert out.count(f"Match positions: {answer}.") == 3 and "Goodbye!" in out


def test_small_modulus_collision_and_invalid_modulus(play):
    out = play("1", "acb", "a", "4", "oops", "1", "1000004", "2", "0", argv=["--topic", "rabin-karp"])
    assert "must be a whole number" in out and "must be at least 2" in out and "must be at most 1000003" in out
    assert "Window 1: hash 1, pattern hash 1" in out and "hash hit at 1 is spurious" in out
    assert "Match positions: [0]." in out and "Verified 1 spurious hash hits" in out


def test_input_caps_preserve_valid_input_after_rejection(play):
    out = play("1", "a" * 81, "abc", "a" * 21, "bc", "2", "0", argv=["--topic", "naive-string-search"])
    assert "text must have at most 80 characters" in out and "pattern must have at most 20 characters" in out
    assert "Match positions: [1]." in out


@pytest.mark.parametrize("length,pattern_length", [(0, 0), (10, 3), (2, 5)])
def test_random_strings_support_empty_and_longer_patterns(play, length, pattern_length):
    out = play("3", str(length), str(pattern_length), "2", "3", "4", "2", "0", argv=["--topic", "string-algorithms"])
    assert f"Text length: {length}; pattern length: {pattern_length}." in out
    assert "Goodbye!" in out


@pytest.mark.parametrize("topic", TOPICS)
@pytest.mark.parametrize("interrupt", [KeyboardInterrupt, EOFError, ":b"])
def test_interrupted_creation_is_clean(play, topic, interrupt):
    tail = ["0", "0"] if interrupt == ":b" else []
    out = play("1", "abc", interrupt, *tail, argv=["--topic", topic])
    assert "Goodbye!" in out and "Traceback" not in out


def test_cancelled_hash_prompt_returns_to_operations(play):
    out = play("2", "4", ":b", "5", ":b", "2", "0", argv=["--topic", "string-algorithms"])
    assert out.count("Cancelled.") == 2 and "Match positions: [2, 8]." in out


@pytest.mark.parametrize("topic,code", [("string-algorithms", "26"), ("naive-string-search", "27"),
                                      ("kmp", "28"), ("rabin-karp", "29")])
def test_topic_quizzes_predictions_and_experiments(play, monkeypatch, topic, code):
    monkeypatch.setattr(random.Random, "shuffle", lambda self, items: None)
    challenge = challenges.make(topic, random.Random(9))
    monkeypatch.setattr(challenges, "make", lambda topic_id: challenge)
    out = play("8", "4", "5", code, "1", "a", "a", "a", "a", "a", "2", repr(challenge.answer),
               "3", "1", "2", "0", "0", "0", "0", "0", "0")
    assert "Quiz score: 5/5" in out and "Correct prediction" in out and "Ratio" in out
    assert progress.current.quizzes[topic].best == 100 and progress.current.challenges[topic] == 1


def test_screen_practice_menu_includes_all_three_experiments(play):
    out = play("2", "10", "3", "1", "2", "2", "2", "3", "2", "0", "0", "0",
               argv=["--topic", "string-algorithms"])
    assert "Naive search: repeated prefix" in out and "KMP: repeated prefix" in out
    assert "Rabin-Karp: repeated prefix" in out and "Goodbye!" in out


@pytest.mark.parametrize("width", [45, 90])
@pytest.mark.parametrize("algorithm,guide", [("2", "2"), ("3", "3"), ("4", "4")])
def test_paused_steps_guides_code_and_comparison_fit_without_color(play, monkeypatch, width, algorithm, guide):
    console.width = width
    monkeypatch.setattr(render, "ascii_art", lambda art: None)
    monkeypatch.setattr(stepper, "can_pause", lambda: True)
    settings.save(settings.Settings(steps="pause", colors=False))
    modulus = ["2"] if algorithm == "4" else []
    code = str(int(algorithm) - 1)
    out = play("2", "1", guide, algorithm, *modulus, "a", "5", "101", "7", code, "0",
               argv=["--topic", "string-algorithms", "--no-color"])
    assert "Step 1:" in out and "\x1b[" not in out
    assert all(cell_len(line) <= width for line in out.splitlines())
    if algorithm == "2":
        assert "=" in out and "!" in out
        if width == 45:
            assert "Alignment split" in out
    elif algorithm == "3":
        assert "KMP prefix table" in out and "avoiding those repeated comparisons" in out
    else:
        assert "spurious" in out and "modulo 2" in out


@pytest.mark.parametrize("width", [45, 90])
def test_typed_repeated_text_fits_after_input_prompts(play, monkeypatch, width):
    console.width = width
    monkeypatch.setattr(render, "ascii_art", lambda art: None)
    out = play("1", "a" * 40, "aaaaab", "3", "0", argv=["--topic", "kmp", "--no-color"])
    assert "Alignment split" in out and all(cell_len(line) <= width for line in out.splitlines())


@pytest.mark.parametrize("width", [45, 90])
def test_long_unicode_control_characters_and_all_code_views_fit(width, capsys):
    console.width, console.no_color = width, True
    text, pattern = ("🦄e\u0301\t[red]\n\x1b" * 6)[:80], "e\u0301\t[red]"
    render.string_data(text, pattern)
    for algorithm in (string_search.naive_search, string_search.kmp_search, string_search.rabin_karp):
        trace = []
        algorithm(text, pattern, trace)
        for i, event in enumerate(trace, 1):
            render.string_step(i, event)
    for note in notes.NOTES:
        if note.topic == "string-algorithms" and note.sources:
            render.code(note)
    out = capsys.readouterr().out
    assert "Alignment split" in out and "\\t" in out and "\\u0301" in out
    assert "\x1b[" not in out and all(cell_len(line) <= width for line in out.splitlines())


@pytest.mark.parametrize("algorithm,modulus", [("2", []), ("3", []), ("4", ["2"])])
def test_paused_steps_can_stop_without_losing_results(play, monkeypatch, algorithm, modulus):
    monkeypatch.setattr(stepper, "can_pause", lambda: True)
    settings.save(settings.Settings(steps="pause"))
    out = play("2", algorithm, *modulus, "s", "0", argv=["--topic", "string-algorithms"])
    assert "Stopped after 1 of" in out and "Match positions: [2, 8]." in out


def test_work_growth_uses_measured_comparisons_and_hash_reads():
    naive, kmp, rabin = experiments.for_topic("string-algorithms")
    sizes = (32, 64, 128)
    naive_rows = experiments.measure(naive, sizes=sizes)
    kmp_rows = experiments.measure(kmp, sizes=sizes)
    rabin_rows = experiments.measure(rabin, sizes=sizes)
    assert [r.work for r in naive_rows] == [(n - n // 4 + 1) * (n // 4) for n in sizes]
    assert all(r.work <= 2 * (r.n + r.n // 4) for r in kmp_rows)
    assert [r.work for r in rabin_rows] == [3 * n - n // 4 + 1 for n in sizes]
    assert naive_rows[-1].work > 10 * kmp_rows[-1].work


def test_flower_power_titles():
    for art in (texts.STRING_ALGORITHMS_ASCII, texts.NAIVE_STRING_SEARCH_ASCII, texts.KMP_ASCII, texts.RABIN_KARP_ASCII):
        assert len(art.splitlines()) >= 9 and "(_ o _)" in art
