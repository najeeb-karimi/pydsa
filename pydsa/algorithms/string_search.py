"""Find every occurrence, including overlaps, with optional narration and comparison counts.

Positions count Python Unicode code points. An empty pattern matches every boundary,
including the end of the text, just as repeated str.find calls do.
"""

from dataclasses import dataclass

from pydsa.algorithms.trace import record

BASE = 256
DEFAULT_MODULUS = 101


@dataclass
class SearchStats:
    """Actual character comparisons; hashing arithmetic is counted separately as windows."""

    comparisons: int = 0
    preprocessing: int = 0
    windows: int = 0
    hash_characters: int = 0
    spurious_hits: int = 0
    reused: int = 0  # Known prefix characters KMP avoids comparing at new alignments.

    @property
    def total(self):
        return self.comparisons + self.preprocessing


def _validate(text, pattern):
    if not isinstance(text, str) or not isinstance(pattern, str):
        raise TypeError("Text and pattern must be strings.")


def _special(text, pattern, trace):
    if not pattern:
        record(trace, "ss_empty", (text, pattern, 0), count=len(text) + 1)
        return list(range(len(text) + 1))
    if len(pattern) > len(text):
        record(trace, "ss_long", (text, pattern, 0), size=len(pattern), length=len(text))
        return []
    return None


def naive_search(text, pattern, trace=None, *, stats=None):
    """Try each possible alignment, stopping its comparisons at the first mismatch."""
    _validate(text, pattern)
    stats = stats if stats is not None else SearchStats()
    special = _special(text, pattern, trace)
    if special is not None:
        return special
    matches = []
    for start in range(len(text) - len(pattern) + 1):
        marks, checks = {}, 0
        stats.windows += 1
        for j, character in enumerate(pattern):
            stats.comparisons += 1
            checks += 1
            equal = text[start + j] == character
            if trace is not None:
                marks[j] = "matched" if equal else "mismatch"
            if not equal:
                break
        else:
            matches.append(start)
        record(trace, "ss_naive", (text, pattern, start), marks,
               start=start, checks=checks, found=checks == len(pattern) and equal)
    return matches


def prefix_table(pattern, trace=None, *, stats=None):
    """Longest proper prefix that is also a suffix for each pattern prefix (the LPS table)."""
    _validate("", pattern)
    stats = stats if stats is not None else SearchStats()
    table, length = [0] * len(pattern), 0
    if pattern and trace is not None:
        record(trace, "ss_prefix_entry", (pattern, tuple(table)), {0: "entry"},
               index=0, length=0, reason="A single character has no nonempty proper prefix")
    for i in range(1, len(pattern)):
        while True:
            stats.preprocessing += 1
            if pattern[i] == pattern[length]:
                length += 1
                reason = "The next characters match, extending the shared prefix and suffix"
                break
            if length == 0:
                reason = "No shorter shared prefix matches this character"
                break
            old = length
            length = table[length - 1]
            if trace is not None:
                record(trace, "ss_prefix_fallback", (pattern, tuple(table)), {i: "checked"},
                       index=i, old=old, length=length)
        table[i] = length
        if trace is not None:
            record(trace, "ss_prefix_entry", (pattern, tuple(table)), {i: "entry"},
                   index=i, length=length, reason=reason)
    return table


def kmp_search(text, pattern, trace=None, *, stats=None):
    """Build the prefix table, then reuse matched prefixes without moving the text cursor back."""
    _validate(text, pattern)
    stats = stats if stats is not None else SearchStats()
    special = _special(text, pattern, trace)
    if special is not None:
        return special
    table = prefix_table(pattern, trace, stats=stats)
    matches, i, j = [], 0, 0
    while i < len(text):
        stats.comparisons += 1
        equal = text[i] == pattern[j]
        if trace is not None:
            marks = {at: "matched" for at in range(j)}
            marks[j] = "matched" if equal else "mismatch"
            record(trace, "ss_compare", (text, pattern, i - j), marks,
                   index=i, position=j, equal=equal)
        if equal:
            i, j = i + 1, j + 1
            if j != len(pattern):
                continue
            matches.append(i - j)
            record(trace, "ss_match", (text, pattern, i - j), start=i - j)
            old_start, j = i - j, table[j - 1]
        else:
            old_start = i - j
            if j:
                j = table[j - 1]
            else:
                i += 1
        stats.reused += j
        stats.windows += 1
        if trace is not None:
            record(trace, "ss_kmp_shift", (text, pattern, i - j),
                   dict.fromkeys(range(j), "matched"), start=old_start, next=i - j, kept=j)
    return matches


def rabin_karp(text, pattern, trace=None, *, modulus=DEFAULT_MODULUS, stats=None):
    """Roll a base-256 polynomial hash; verify every hash hit character by character.

    A small modulus intentionally produces more collisions without changing the answers.
    Any integer modulus of at least two is accepted; primality is not needed for correctness.
    """
    _validate(text, pattern)
    if type(modulus) is not int or modulus < 2:
        raise ValueError("The hash modulus must be an integer of at least 2.")
    stats = stats if stats is not None else SearchStats()
    special = _special(text, pattern, trace)
    if special is not None:
        return special
    m = len(pattern)
    high = pow(BASE, m - 1, modulus)
    pattern_hash, window_hash = 0, 0
    for i in range(m):
        stats.hash_characters += 2
        pattern_hash = (pattern_hash * BASE + ord(pattern[i])) % modulus
        window_hash = (window_hash * BASE + ord(text[i])) % modulus
    matches = []
    for start in range(len(text) - m + 1):
        stats.windows += 1
        record(trace, "ss_hash_window", (text, pattern, start),
               start=start, window=window_hash, pattern_hash=pattern_hash, modulus=modulus, base=BASE)
        if window_hash == pattern_hash:
            marks, checks = {}, 0
            for j in range(m):
                stats.comparisons += 1
                checks += 1
                equal = text[start + j] == pattern[j]
                if trace is not None:
                    marks[j] = "matched" if equal else "mismatch"
                if not equal:
                    break
            else:
                matches.append(start)
            found = checks == m and equal
            if not found:
                stats.spurious_hits += 1
            record(trace, "ss_hash_hit" if found else "ss_collision", (text, pattern, start), marks,
                   start=start, checks=checks)
        if start + m < len(text):
            stats.hash_characters += 2
            outgoing, incoming, old = ord(text[start]), ord(text[start + m]), window_hash
            window_hash = ((window_hash - outgoing * high) * BASE + incoming) % modulus
            record(trace, "ss_roll", (text, pattern, start + 1), start=start + 1,
                   old=old, outgoing=outgoing, incoming=incoming, high=high, window=window_hash, modulus=modulus, base=BASE)
    return matches
