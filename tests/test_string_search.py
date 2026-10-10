"""All occurrences compared with str.find; prefix borders, rolling hashes and work counts checked independently."""

import itertools
import random

import pytest

from pydsa.algorithms import string_search as strings

SEARCHES = (strings.naive_search, strings.kmp_search, strings.rabin_karp)


def occurrences(text, pattern):
    result, start = [], 0
    while start <= len(text):
        index = text.find(pattern, start)
        if index < 0:
            break
        result.append(index)
        start = index + 1
    return result


def borders(pattern):
    return [max((size for size in range(i + 1) if pattern[:size] == pattern[i + 1 - size:i + 1]), default=0)
            for i in range(len(pattern))]


@pytest.mark.parametrize("text,pattern", [
    ("", ""), ("", "a"), ("abc", ""), ("abc", "abcdef"), ("abc", "abc"), ("aaaaa", "aa"),
    ("abababa", "aba"), ("abc", "x"), ("ABCabc", "abc"), ("   ", " "), ("x  x ", "x "),
    ("line\nline\tline", "line"), ("🦄é🦄é", "🦄é"), ("e\u0301e\u0301", "e\u0301"),
    ("abc\0abc", "\0"), ("[red]x[red]", "[red]"),
])
@pytest.mark.parametrize("search", SEARCHES, ids=lambda search: search.__name__)
def test_edge_cases_match_str_find(search, text, pattern):
    trace, stats = [], strings.SearchStats()
    assert search(text, pattern, trace, stats=stats) == occurrences(text, pattern)
    assert search(text, pattern) == occurrences(text, pattern)
    assert stats.total >= 0


@pytest.mark.parametrize("search,options", [
    (strings.naive_search, {}), (strings.kmp_search, {}),
    (strings.rabin_karp, {"modulus": 2}), (strings.rabin_karp, {"modulus": 3}),
    (strings.rabin_karp, {"modulus": 101}), (strings.rabin_karp, {"modulus": 1000003}),
], ids=["naive", "KMP", "RK-2", "RK-3", "RK-101", "RK-large"])
def test_random_unicode_inputs_match_str_find(search, options):
    rng = random.Random(50)
    alphabet = "aab cABé🦄\u0301\n\t\0"
    for _ in range(800):
        text = "".join(rng.choice(alphabet) for _ in range(rng.randrange(65)))
        pattern = "".join(rng.choice(alphabet) for _ in range(rng.randrange(21)))
        if text and rng.random() < .4:
            start = rng.randrange(len(text))
            pattern = text[start:start + rng.randrange(12)]
        trace = []
        assert search(text, pattern, trace, **options) == occurrences(text, pattern)
        assert search(text, pattern, **options) == occurrences(text, pattern)


def test_exhaustive_binary_strings():
    texts = ["".join(chars) for n in range(7) for chars in itertools.product("ab", repeat=n)]
    patterns = ["".join(chars) for n in range(5) for chars in itertools.product("ab", repeat=n)]
    for text in texts:
        for pattern in patterns:
            reference = occurrences(text, pattern)
            assert all(search(text, pattern) == reference for search in SEARCHES)


def test_prefix_table_matches_brute_force_borders_and_snapshots():
    rng = random.Random(71)
    for _ in range(300):
        pattern = "".join(rng.choice("abc") for _ in range(rng.randrange(60)))
        trace, stats = [], strings.SearchStats()
        table = strings.prefix_table(pattern, trace, stats=stats)
        reference = borders(pattern)
        assert table == reference
        assert stats.preprocessing == max(0, len(pattern) - 1) + sum(e.kind == "ss_prefix_fallback" for e in trace)
        entries = [e for e in trace if e.kind == "ss_prefix_entry"]
        assert len(entries) == len(pattern)
        for i, event in enumerate(entries):
            assert event.data["index"] == i and event.data["length"] == reference[i]
            assert event.snapshot[1][:i + 1] == tuple(reference[:i + 1])
            assert event.data["reason"]
        if table:
            table[-1] = 9999
            assert entries[-1].snapshot[1] == tuple(reference)


def polynomial(value, modulus):
    return sum(ord(char) * strings.BASE ** (len(value) - i - 1) for i, char in enumerate(value)) % modulus


@pytest.mark.parametrize("modulus", [2, 3, 101, 1000003])
def test_rolling_hashes_match_fresh_hashes_and_verify_collisions(modulus):
    rng = random.Random(2)
    for _ in range(100):
        text = "".join(rng.choice("abé🦄") for _ in range(30))
        pattern = "".join(rng.choice("abé🦄") for _ in range(rng.randint(1, 8)))
        trace, stats = [], strings.SearchStats()
        result = strings.rabin_karp(text, pattern, trace, modulus=modulus, stats=stats)
        windows = [e for e in trace if e.kind == "ss_hash_window"]
        assert len(windows) == stats.windows == len(text) - len(pattern) + 1
        assert stats.hash_characters == 2 * len(text)
        for start, event in enumerate(windows):
            assert event.data["start"] == start
            assert event.data["window"] == polynomial(text[start:start + len(pattern)], modulus)
            assert event.data["pattern_hash"] == polynomial(pattern, modulus)
        hits = [e for e in trace if e.kind in ("ss_hash_hit", "ss_collision")]
        assert stats.comparisons == sum(e.data["checks"] for e in hits)
        assert stats.spurious_hits == sum(e.kind == "ss_collision" for e in hits)
        assert result == occurrences(text, pattern)
        for event in hits:
            start = event.data["start"]
            assert (event.kind == "ss_hash_hit") == (text[start:start + len(pattern)] == pattern)


def test_small_modulus_exposes_spurious_hit_without_false_match():
    trace, stats = [], strings.SearchStats()
    assert strings.rabin_karp("acb", "a", trace, modulus=2, stats=stats) == [0]
    assert stats.spurious_hits == 1
    assert [e.data["start"] for e in trace if e.kind == "ss_collision"] == [1]


def test_comparison_counts_and_kmp_prefix_reuse_are_real():
    text, pattern = "a" * 128, "a" * 15 + "b"
    counts = []
    for search in SEARCHES:
        trace, stats = [], strings.SearchStats()
        assert search(text, pattern, trace, stats=stats) == []
        counts.append(stats.total)
        if search is strings.naive_search:
            assert stats.comparisons == (len(text) - len(pattern) + 1) * len(pattern)
            assert stats.comparisons == sum(e.data["checks"] for e in trace)
        if search is strings.kmp_search:
            assert stats.comparisons == sum(e.kind == "ss_compare" for e in trace)
            assert stats.reused == sum(e.data["kept"] for e in trace if e.kind == "ss_kmp_shift")
            assert stats.reused > 0 and stats.total <= 2 * (len(text) + len(pattern))
    assert counts[1] < counts[0] and counts[2] == 0  # Hash work still occurred.
    naive, kmp = strings.SearchStats(), strings.SearchStats()
    strings.naive_search("abc", "abc", stats=naive)
    strings.kmp_search("abc", "abc", stats=kmp)
    assert kmp.total > naive.total  # Honest totals include preprocessing on a tiny input.


@pytest.mark.parametrize("search", SEARCHES)
@pytest.mark.parametrize("text,pattern", [(None, "a"), ("a", 3), (["a"], "a"), (True, "")])
def test_non_string_inputs_are_rejected(search, text, pattern):
    with pytest.raises(TypeError, match="must be strings"):
        search(text, pattern)


@pytest.mark.parametrize("modulus", [0, 1, -5, True, 2.5, "101"])
def test_invalid_moduli_are_rejected_even_on_empty_input(modulus):
    with pytest.raises(ValueError, match="modulus"):
        strings.rabin_karp("", "", modulus=modulus)
