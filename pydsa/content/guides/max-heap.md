# Max Heap
> A max heap keeps the largest key at its root, and every parent is larger than or equal to its children. It's a min heap turned upside down, with the biggest key always ready.

## What it is
A max heap is a [complete binary tree](glossary:complete-binary-tree) stored in an array, where every parent's [key](glossary:key) is larger than or equal to the keys of its children. That's the [heap property](glossary:heap-property) of a max heap. Like a min heap, it only promises an order between parents and their children, not between siblings.

## How it works
A max heap works exactly like a min heap with every comparison flipped:
- `Insert` appends the key as the last leaf and [sifts it up](glossary:sifting) while it's larger than its parent.
- `Extract Max` moves the last leaf into the root's place and sifts it down, swapping it with its larger child while that child is larger.
- `Peek Max` reads the root.
- `Build from a List` sifts down every parent, from the last parent back to the root, using [heapify](glossary:heapify).

The smallest key in a max heap is always one of the [leaves](glossary:leaf).

## Real-life analogy
A leaderboard that only has to show the top score. Whenever the champion leaves, the best of the remaining players quickly moves up to take the top spot.

## When to use it
- You always want the largest item next, like the highest bid or the most urgent job.
- Heap Sort, which builds a max heap and then keeps moving the largest key to the end of the list.
- Keeping the 10 smallest items you've seen so far: in a max heap of those 10, the largest sits at the root, ready to be dropped when a smaller item shows up.

## When to avoid it
- You need the smallest item; use a min heap.
- You need to search for keys or keep all of them sorted.

## In PyDSA
- You choose whether the heap holds numbers or strings, and duplicate keys are allowed.
- Every operation that moves keys shows each step as a tree and as the array.
- The example builds a max heap from the same keys as the min heap example, so you can compare the two.
