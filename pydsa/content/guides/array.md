# Array
> An array is a row of numbered boxes that all hold the same kind of value. Because every box has a number, you can jump straight to any of them.

## What it is
An array is a [data structure](glossary:data-structure) that stores a fixed number of values side by side. Each position has an [index](glossary:index), starting at 0 for the first one, so an array of 5 values has the indexes 0 to 4. All the values have the same type, such as whole numbers or text.

## How it works
The values sit next to each other in [contiguous memory](glossary:contiguous-memory). To find the value at index 3, the computer takes the address of the first box and moves forward 3 boxes. That's one small calculation, so reading or writing the last index is just as fast as reading the first.

- `Get by Index` reads the value at an index.
- `Insert` stores a value at an index, replacing the value that was there.
- `Delete` clears an index by resetting it to a default value.
- `Search` looks through the values for a target, and `Sort` puts them in order.

The price of this speed is the fixed size. The boxes are reserved when the array is created, so it can't grow later. Making room for more values means creating a bigger array and copying every value over.

## Real-life analogy
A row of numbered lockers. You can walk straight to locker 42 without opening lockers 0 to 41, but the row has exactly as many lockers as were built, and every locker is the same size.

## When to use it
- You know how many values you need, at least roughly.
- You read values by position much more often than you add or remove them.
- You want values stored compactly, one after another, like the pixels of an image or the temperatures of every day in a month.

## When to avoid it
- The number of values changes a lot. A [dynamic array](glossary:dynamic-array), such as Python's `list`, or a linked list fits better.
- You often insert or remove values in the middle while keeping the rest in order, because every value after that spot has to shift.

## In PyDSA
- You choose the size and the data type, `int` or `str`, when you create the array, and neither can change afterward.
- `Insert` overwrites the value at an index instead of shifting the others. `Delete` resets an index to the default value, which is `0` for an `int` array and an empty string for a `str` array.
- An index outside 0 to the size minus 1 is rejected, so you can never write past the end.
- `Sort` and `Search` let you try every sorting and searching algorithm on the array and watch what each one does.
