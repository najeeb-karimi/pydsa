# Radix Sort
> Radix Sort sorts whole numbers one digit at a time, starting with the ones digit, by dealing them into ten buckets and collecting the buckets in order. After the last digit, the whole list is sorted.

## What it is
Radix Sort is a non-comparison sort for whole numbers. Instead of comparing numbers, it looks at their digits. PyDSA's version starts with the least significant digit: it sorts by the ones digit, then by the tens digit, then by the hundreds digit, and so on.

## How it works
1. Deal every number into one of ten [buckets](glossary:bucket), numbered 0 to 9, by its ones digit. Numbers in the same bucket keep the order they arrived in.
2. Collect the buckets from 0 to 9 back into the list.
3. Repeat with the tens digit, then the hundreds digit, until you've used every digit of the largest number.

For example, sorting `[170, 45, 75, 90]` by the ones digit gives `[170, 90, 45, 75]`, and then by the tens digit gives `[45, 170, 75, 90]`. Sorting by the hundreds digit finishes the job: `[45, 75, 90, 170]`.

The trick is that every pass is [stable](glossary:stable-sort). Numbers with the same digit keep the order the earlier passes gave them, so the order from the smaller digits survives, and the final pass leaves everything sorted.

## Real-life analogy
Sorting a stack of numbered tickets with a row of ten trays. You deal the tickets into the trays by their last digit and stack them back up, then deal them by the digit before that, and so on. After the first digit, the whole stack is in order.

## When to use it
- Large lists of whole numbers with few digits, like postal codes, phone numbers or IDs.
- Keys that all have the same length, such as dates written as numbers.

## When to avoid it
- Numbers with many digits, or a mix of very small and very large numbers, which need many passes.
- Values that aren't whole numbers.
- Memory is tight, since the buckets hold a copy of every number during each pass.

## In PyDSA
- Radix Sort only accepts `int` values that aren't negative, and it tells you when a list doesn't fit.
- For descending order, the buckets are collected from 9 down to 0.
- A step is shown after every digit, so there are as many steps as the largest number has digits.
