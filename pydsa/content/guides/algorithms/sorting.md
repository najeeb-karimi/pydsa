# Sorting
> Sorting puts a collection in order, such as numbers from smallest to largest or words from A to Z. Different sorting algorithms reach the same result in very different ways, and some are much faster than others.

## What it is
A sorting [algorithm](glossary:algorithm) rearranges a list so every item comes after the items that belong before it. Sorted data is easier for people to read and much easier for computers to work with: it allows binary search, puts equal items next to each other, and is the first step of many other algorithms.

Sorting algorithms come in two families:
- [Comparison sorts](glossary:comparison-sort) decide the order by comparing two items at a time. Bubble, Selection, Insertion, Quick, Heap, Shell and Merge Sort are all comparison sorts.
- Non-comparison sorts, such as Counting Sort and Radix Sort, look at the values themselves. That only works for certain kinds of values, like whole numbers.

## How it works
Every sorting algorithm answers the same question, where each item belongs, with a different strategy:
- Swap neighbors that are out of order until nothing moves: Bubble Sort.
- Pick the smallest remaining item and put it next: Selection Sort.
- Take the items one at a time and insert each into the sorted part: Insertion Sort, and Shell Sort, which starts with big gaps.
- Split the list, sort the parts and combine them: Quick Sort and Merge Sort, which are [divide and conquer](glossary:divide-and-conquer) algorithms.
- Use a heap to pull out the largest item again and again: Heap Sort.
- Count or bucket the values instead of comparing them: Counting Sort and Radix Sort.

Three things are worth watching when you compare them: how much more work they do as the list grows, how much extra memory they need, and whether they're [stable](glossary:stable-sort), keeping equal items in their original order.

## Real-life analogy
Sorting a hand of playing cards. Some people pick up one card at a time and slide it into place, others spread the cards out and pick the lowest one each time, and some split the hand into suits first. Everyone ends up with a sorted hand.

## When to use it
- You'll search the data many times, so sorting it once lets every search use Binary Search.
- You need to find duplicates, the median, or the smallest and largest items.
- You're showing data to people, like a leaderboard or an alphabetical list of names.

## When to avoid it
- You only need the few smallest or largest items; a heap finds them without sorting everything.
- You only search once or twice; a Linear Search is cheaper than sorting first.
- The data changes all the time, and sorting it again after every change would be wasteful; a balanced tree keeps it in order as it changes.

## In PyDSA
- Every algorithm sorts a copy of your list, so you can try them all on the same data. The array screen sorts the array itself.
- You choose ascending or descending order. Every run shows each step with the values that moved highlighted, and counts the comparisons and writes it took.
- `Compare All Algorithms` runs every algorithm on the same list and shows their work side by side. Try a sorted list, a reversed one and one full of duplicates.
- Counting Sort and Radix Sort only accept whole numbers, and PyDSA tells you when a list doesn't fit.
