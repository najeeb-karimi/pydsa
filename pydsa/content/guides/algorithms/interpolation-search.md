# Interpolation Search
> Interpolation Search guesses where the target should be from its value, instead of always checking the middle. On evenly spread numbers, its guesses land so close that it needs even fewer checks than Binary Search.

## What it is
Interpolation Search is a search for sorted numbers. Binary Search always checks the middle, but when you're looking for a value close to the largest one, it makes more sense to look near the end. Interpolation Search estimates the position from how far the target is between the smallest and largest values of the range.

## How it works
1. Keep a range from a low position to a high position, starting with the whole list.
2. If the target is smaller than the lowest value or larger than the highest value in the range, it isn't there.
3. Estimate the position as `low + (target − values[low]) × (high − low) ÷ (values[high] − values[low])`, rounded down.
4. If the value at that position is the target, you've found it. If it's smaller, the range now starts after the position, and if it's larger, the range now ends before it.
5. Repeat from step 2.

For example, in `[10, 20, 30, 40, 50]`, the target 40 is three quarters of the way from 10 to 50, so the first guess is position 3, which is exactly right.

When the numbers are spread out evenly, the guesses are very accurate. When they're bunched up, like `[1, 2, 3, 4, 1000]`, the guesses can be far off, and the search may end up checking almost every value.

## Real-life analogy
Looking up "Williams" in a phone book. You don't open it in the middle; you open it near the end, because W is near the end of the alphabet.

## When to use it
- Large sorted lists of numbers that are spread out fairly evenly, like IDs handed out in order or readings taken at regular times.

## When to avoid it
- The numbers are spread unevenly; Binary Search is safer.
- The values aren't numbers, since the guess needs arithmetic.

## In PyDSA
- Interpolation Search only accepts lists of numbers, and it tells you when a list doesn't fit.
- It runs on a sorted copy of your list and reports the index where the target first appears in your original list.
- Try it on the example list and on a random list, and compare how many positions it checks.
