# Fenwick Tree
> A Fenwick tree stores sums of overlapping array blocks. Binary index jumps let it answer prefix and range sums and update one value without visiting every position.

## What it is
A Fenwick tree, also called a binary indexed tree, keeps an auxiliary array of block sums. It is designed for changing numeric arrays and repeated sums. Unlike a search tree, its links are calculated from indexes rather than stored as pointers.

## How it works
Internal indexes start at 1. Block i contains i & -i values ending at i: the lowest set bit of i gives the block's length. For instance, internal 6 is binary 0110, whose lowest set bit is 0010; its block covers public array positions 4 and 5.

Construction starts each block with its own array value and passes completed blocks to their parent using i + (i & -i). Each block is passed once, so construction avoids repeated point updates.

A prefix sum starts at the internal index for its public end, adds that block and removes its lowest set bit. Repeating i − (i & -i) reaches 0 without counting any value twice. A range sum subtracts the prefix before the start from the prefix at the end.

A point update replaces one array value. Its difference from the old value is added to every affected block, jumping upward with i + (i & -i). The typed value is a replacement, not an amount to add.

Integer sums stay exact. Floating-point sums can round, and subtracting nearly equal large prefixes can lose a small range sum; use integers when exact totals matter.

## Real-life analogy
Think of a running account with saved subtotals for blocks of transactions. To total everything through a date, combine non-overlapping blocks backward. Correcting one transaction adjusts only the saved blocks that contain it.

## When to use it
Use it for repeated prefix or range sums mixed with point changes. Its compact block array is useful when sums are the only aggregate you need.

## When to avoid it
Use a segment tree for arbitrary minimum or maximum queries: subtracting two prefix minima or maxima does not recover a range answer. For a static array, an ordinary prefix-sum array is simpler. This implementation does not support range updates.

## In PyDSA
Type finite numbers, load the example or generate up to 50 random values. Public array indexes start at 0, and range ends are inclusive. Prefix end −1 gives an empty sum of 0. The block table shows internal indexes and lowest set bits in binary, alongside their public ranges. Steps show the bit being added or removed and the next index in binary. Build from Array replaces all data; Point Update replaces one value. Practice includes quizzes, fresh predictions and experiments comparing block visits with reading the same range directly; construction and trace snapshots are excluded from the work count.
