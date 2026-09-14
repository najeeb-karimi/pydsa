# Jump Search
> Jump Search moves through a sorted list in jumps of a fixed size, checking the last value of each block. Once it finds the block that could hold the target, it checks that block one value at a time.

## What it is
Jump Search is a search for sorted data that sits between Linear Search and Binary Search. It skips over whole blocks of values instead of checking each one, and it only ever moves forward through the list.

## How it works
1. Choose a block size. The best size is the square root of the list's length, so a list of 16 values uses blocks of 4.
2. Check the last value of the first block. If it's smaller than the target, the target can't be in this block, so jump to the next block.
3. Keep jumping until the last value of a block is greater than or equal to the target, or the list ends.
4. Go back to the start of that block and check its values one by one, until you find the target or pass the place where it would be.

With blocks the size of the square root of the length, there are never more jumps than there are values in a block, which keeps both parts of the search short.

## Real-life analogy
Looking for a page in a book by flipping ahead ten pages at a time. Once you've flipped past the page you want, you go back and turn the last few pages one by one.

## When to use it
- Sorted data where going backward is expensive, like data read from a tape, since Jump Search only moves forward.
- You want something faster than Linear Search that's still simple to write.

## When to avoid it
- You can jump to any position cheaply, as in an array; Binary Search needs fewer checks.
- The data isn't sorted.

## In PyDSA
- The block size is the whole-number square root of the length, so a list of 8 values uses blocks of 2.
- Jump Search runs on a sorted copy of your list and reports the index where the target first appears in your original list.
- The numbered positions show the jumps first, then the checks inside the final block.
