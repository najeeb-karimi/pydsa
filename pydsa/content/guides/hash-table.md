# Hash Table
> A hash table stores key-value pairs and uses a hash function to turn each key into the position where its pair belongs. Instead of searching, it computes where to look, so lookups are usually almost instant.

## What it is
A hash table is a [data structure](glossary:data-structure) for key-value pairs, like names and their phone numbers. It has an array of positions, called [buckets](glossary:bucket) or slots. A [hash function](glossary:hash-function) turns any [key](glossary:key) into a number, and that number, wrapped around to the size of the table, is the key's position.

Two different keys can end up at the same position. That's called a [collision](glossary:collision), and every hash table needs a way to handle it. The two main families are:
- Separate chaining, where each bucket holds a small list of every pair that lands there.
- Open addressing, where each slot holds a single pair, and a colliding key looks for another free slot. Linear probing is the simplest version.

## How it works
To insert, search for or delete a key, the table first computes the key's position with the hash function, then only works at that position:
- With separate chaining, it goes through that bucket's short list.
- With linear [probing](glossary:probing), it checks the key's home slot and then the slots after it, one by one, until it finds the key or an empty slot.

When the keys are spread out evenly and the table isn't too full, each position holds only a few keys, so these operations take about the same short time however many keys the table holds. When many keys collide, the work at one position grows, and the table slows down.

## Real-life analogy
A coat check. When you hand over your coat, you get a ticket with a hook number, and later the attendant walks straight to that hook instead of searching through every coat. If two coats get the same number, they share the hook, or one goes on the next free hook.

## When to use it
- Looking things up by key, like a dictionary, a phone book or a cache of web pages.
- Counting things, like how many times each word appears in a book.
- Checking quickly whether you've already seen something.

## When to avoid it
- You need the keys in sorted order, the smallest key, or every key in a range; a balanced tree keeps its keys in order.
- Memory is very tight, since a hash table keeps spare room to avoid collisions.

## In PyDSA
- After the hash table opens, you choose separate chaining, linear probing or the hash set. You can also open one directly with its topic ID.
- Keys and values can be of any type, and inserting a key that's already there updates its value.
- The hash function is Python's `hash()` of the key, wrapped around to the size of the table. Python gives strings different hash codes each time it starts, so string keys can land in different positions from one run to the next.
