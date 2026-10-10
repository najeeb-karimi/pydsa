# Segment Tree
> A segment tree stores answers for nested ranges of an array. Choose sum, minimum or maximum, then reuse those answers when querying a range or replacing a value.

## What it is
A segment tree is a [binary tree](glossary:binary-tree) over array positions rather than sorted keys. Each [node](glossary:node) stores an inclusive range and its combined value. The root covers the whole array; each leaf covers one position.

## How it works
Building divides a range near its middle until each part holds one value. Then each parent combines its two children using the operation chosen at creation: sum, minimum or maximum.

A query classifies each visited node. A fully inside node supplies its saved answer. A partly overlapping node sends the query into both children. An outside node contributes nothing. Combining the covered pieces gives the answer without reading every array value. A whole-array query can use the root alone.

A point update replaces a leaf's value and recomputes only its ancestors. It does not add the typed value to the old one. Array length stays fixed until you build from a new array.

Integer sums stay exact. Floating-point sums can round because the tree groups additions differently from reading the array left to right.

## Real-life analogy
Imagine a sales report with totals for the whole year, halves, quarters and smaller periods. To total a particular span, use the largest saved periods that fit and combine them, instead of reading every receipt. Correcting one receipt only changes its enclosing reports.

## When to use it
Use it for repeated range queries mixed with individual changes, especially when you need minimum or maximum as well as sums.

## When to avoid it
For a few small queries, reading the array directly is simpler. For sums alone, a Fenwick tree uses less storage. This implementation has point updates; it does not support changing a whole range at once.

## In PyDSA
Create an array of finite numbers, load the example or generate up to 50 random values. Choose Sum, Minimum or Maximum for any create mode. Public indexes start at 0, and both range ends are included. Query steps label nodes inside, partial or outside, even with colors off. Build from Array replaces all data while keeping the chosen operation; Point Update replaces one value. Guides, code views, quizzes and fresh predictions are available. Experiments compare visited query nodes with reading the same range directly; input construction and trace snapshots are excluded from the work count.
