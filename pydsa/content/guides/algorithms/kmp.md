# Knuth-Morris-Pratt (KMP)
> KMP finds every pattern occurrence while reusing earlier character matches. Its prefix table tells it how far the pattern can shift without restarting those comparisons.

## What it is
KMP is an exact string-search algorithm named after Knuth, Morris and Pratt. Each prefix-table entry, often called LPS, is the length of the longest proper prefix that is also a suffix of the pattern up to that index. Proper means the prefix is shorter than the whole piece being considered.

## How it works
1. Set the first prefix entry to zero: one character has no nonempty proper prefix.
2. For each later character, extend the current shared prefix if the next characters match.
3. On a mismatch, try the shorter prefix saved in the earlier table. Store zero if none matches.
4. Search with a text cursor and a matched pattern length. Matching characters advance both.
5. On a mismatch, reuse the shorter prefix from the table instead of moving the text cursor backward.
6. On a full match, record its start and keep the longest prefix that is also a suffix so overlaps can still match.

For `abab`, the table is `[0, 0, 1, 2]`. After matching that pattern, two characters are already known to match at the next overlapping alignment. Prefix reuse avoids rechecking those characters. Building the table also costs comparisons, which must be included in an honest comparison.

## Real-life analogy
When reading a repeated phrase, remember the part you have already recognized. A failed continuation does not force you to reread every earlier letter if the phrase itself tells you which suffix can start another match.

## When to use it
- Repeated text and pattern prefixes cause naive search to redo work.
- You want predictable growth without relying on hash collisions being rare.

## When to avoid it
- A tiny search makes preprocessing unnecessary overhead.
- You need approximate matches or different character-equality rules.

## In PyDSA
- The prefix table is built step by step with a reason for each completed entry and any fallback.
- Search steps show character comparisons and each pattern shift, including the known prefix that avoids repeated comparisons.
- The comparison table separates search and prefix work; reported prefix reuse is not a promise that total work beats naive search on every input.
- Typed strings, examples, random strings, code views, quizzes, predictions and a growth experiment are available.
