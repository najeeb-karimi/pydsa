# Naive String Search
> Naive string search tries the pattern at every possible starting position. It stops an alignment at the first mismatch and reports every complete match, including overlaps.

## What it is
Naive search is the direct way to find an exact substring. It keeps no prefix table or hash: the original characters decide whether each alignment matches.

## How it works
1. Place the pattern under the beginning of the text.
2. Compare characters from left to right until a mismatch or the end of the pattern.
3. Record the starting position if the whole pattern matches.
4. Shift by one character, even after a match, so overlapping matches are found.
5. Repeat until there is no room for the whole pattern.

An empty pattern matches all boundaries. If the pattern is longer than the text, there is no valid alignment. Long repeated prefixes can make the same characters get compared many times.

## Real-life analogy
Slide a paper strip with a word written on it across a line of print. At each position, compare letters in order and move the strip one place after a mismatch.

## When to use it
- A short text or pattern makes a simple search enough.
- You want a clear baseline for comparing other searches.

## When to avoid it
- Long repeated prefixes cause many comparisons at each shift.
- You search large texts repeatedly and can benefit from KMP or hash filtering.

## In PyDSA
- Use typed strings, the example or random data on the String Algorithms screen.
- Every alignment draws the pattern under the text. Matching characters are marked with = and the first mismatch with !, including when colors are off.
- Long alignments split into chunks with their original character indexes.
- Compare all three searches, inspect the code, practice predicting match positions or measure repeated-prefix growth.
