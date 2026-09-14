# Counting Sort
> Counting Sort doesn't compare values at all: it counts how many times each value appears, then writes the values back in order. For whole numbers in a small range, it beats every comparison sort.

## What it is
Counting Sort is a non-comparison sort for whole numbers. Instead of asking which of two values comes first, it uses the values themselves as positions in a list of counters, with one counter for every possible value between the smallest and the largest.

## How it works
1. Find the smallest and largest values, and make one counter for every value from the smallest to the largest.
2. Go through the list and add 1 to the counter of each value.
3. Go through the counters in order. For each counter, write its value back into the list as many times as it was counted.

For example, `[3, 1, 3, 2]` gives a count of 1 for the value 1, 1 for the value 2 and 2 for the value 3, so the list is written back as `[1, 2, 3, 3]`.

Negative numbers work too: subtracting the smallest value from every value turns the smallest value into counter 0.

The work depends on the length of the list plus the size of the range. A few numbers spread far apart need a huge number of counters, most of them zero.

## Real-life analogy
Counting the votes of an election with a few candidates. You never compare two ballots; you add a tally mark for a candidate on each ballot and read off the totals at the end.

## When to use it
- Whole numbers in a small range, like ages, test scores out of 100 or the days of a month.
- As a building block of Radix Sort, which sorts by one digit at a time.

## When to avoid it
- The values are spread over a huge range; the counters would take far more memory and time than the list itself.
- The values aren't whole numbers, such as decimals or words.

## In PyDSA
- Counting Sort only accepts lists of `int` values that are less than 10,000 apart, and it tells you when a list doesn't fit.
- It never compares values, so its comparison count is always 0.
- A step is shown after all the copies of one value have been written back.
