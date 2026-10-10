# Bloom Filter
> A Bloom filter uses a bit array to rule out items that were never added. A positive answer means only “might contain”: different items can set the same bits.

## What it is
A Bloom filter is a probabilistic membership structure. It stores bits instead of the original items. Each item has several hash positions. If any of its positions is 0, it is definitely absent; if all are 1, it might have been added.

## How it works
Choose m bits and k hash functions. Adding a string sets its k positions to 1. Checking a string examines those positions and can stop at the first 0. Adding more items never clears bits, so an added item never becomes a negative result.

Other strings can set all the positions of a string you never added. That is a false positive. A positive check must be confirmed in the original data when certainty matters. Ordinary deletion is unsupported: clearing a bit could hide another item that shares it.

PyDSA hashes UTF-8 strings with SHA-256 and a separate fixed salt for each hash number. These positions stay stable across processes, unlike Python's randomized string hash. Each array position is stored as a byte containing 0 or 1 for readable teaching code.

For n distinct additions, a usual approximation for the false positive rate is (1 − exp(−k × n / m))^k. It assumes independent uniform hashes and is not an exact guarantee for finite filters. The [Apache Commons Bloom-filter introduction](https://commons.apache.org/proper/commons-collections/bloomFilters/intro.html) explains the formula and its limits. Repeated additions do not represent new distinct items, and adding more hashes is not always better for a fixed bit count and load.

## Real-life analogy
Imagine a quick checklist that can tell you a book is definitely not in a library. A possible match sends you to the real catalog; the checklist cannot prove the library owns the book.

## When to use it
Use it as a preliminary filter before an expensive exact lookup when occasional false positives are acceptable. It is also useful for seeing the tradeoff between space, hash count and the number of stored items.

## When to avoid it
Use a hash set when you need exact membership, original items or deletion. A crowded filter can answer “might contain” for almost everything. This implementation demonstrates the algorithm rather than providing packed production storage.

## In PyDSA
Choose 1 to 512 bits and 1 to 10 hashes, load the 32-bit example or generate random words. The core accepts any positive integer m and k. Add and Might Contain narrate each salted hash position, with text markers when colors are off. Positive results explain false positives. The display counts Add calls, including repeats; it does not claim that count is the number of distinct items. Practice includes quizzes, fresh predictions and a bounded experiment that compares measured false positives on known-absent strings with the approximate formula as distinct additions grow.
