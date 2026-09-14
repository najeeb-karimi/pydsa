# Deque
> A deque, pronounced "deck", is a double-ended queue: you can add and remove items at both its front and its back. It can act as a stack, as a queue, or as a mix of both.

## What it is
A deque is a [data structure](glossary:data-structure) that keeps items in a line with two open ends. A stack has one open end, and a queue adds at one end and removes at the other, but a deque lets you push, pop and peek at either end.

Using only one end gives you a stack, which is [LIFO](glossary:lifo). Pushing at one end and popping at the other gives you a queue, which is [FIFO](glossary:fifo).

## How it works
The operations come in pairs, one for each end: `Push Front` and `Push Back`, `Pop Front` and `Pop Back`, and `Peek Front` and `Peek Back`.

A deque stored in a [circular array](glossary:circular-array) remembers which slot holds its front item and how many items it has. Pushing onto the front steps the front back by one slot, and pushing onto the back writes into the slot after the last item. Both ends wrap around the array, so stepping back from slot 0 lands on the last slot. No item ever moves, which makes every operation at either end equally fast.

## Real-life analogy
A deck of cards on a table, where you may put a card on or take a card from the top or the bottom, but never from the middle.

## When to use it
- An undo history with a limit: push new actions onto one end, and drop the oldest from the other end once the history is full.
- Sliding window problems, such as finding the largest value in every group of 5 neighbors in a list.
- Checking whether a word is a palindrome by comparing the letters popped from both ends.
- Schedulers that take work from either end of a line.

## When to avoid it
- You only ever use one end, or always add at one end and remove at the other. A plain stack or queue says what you mean more clearly.
- You need to reach items in the middle.

## In PyDSA
- The deque is a circular deque with a fixed size. You choose its [capacity](glossary:capacity), and pushing onto a full deque is rejected.
- It holds items of any type.
- The display marks the front and back slots. A popped item stays in its slot, struck out, until a later push overwrites it.
- In the example, pushing onto the front wraps around to the last slot of the array.
