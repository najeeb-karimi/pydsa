# Separate Chaining Hash Table
> A separate chaining hash table gives every bucket a list, and every key that hashes to that bucket joins its list. Collisions never cause trouble, and the table never fills up.

## What it is
Separate chaining, also called open hashing, is a way to handle [collisions](glossary:collision) in a hash table. Each [bucket](glossary:bucket) holds a chain: a small list of the key-value pairs whose [key](glossary:key) hashes to that bucket. Keys that collide simply share a chain.

## How it works
- To insert a pair, the table computes the key's bucket with the [hash function](glossary:hash-function) and goes through that bucket's chain. If the key is already there, its value is updated. Otherwise, the pair is added to the end of the chain.
- To search, it computes the bucket and goes through its chain until it finds the key or the chain ends.
- To delete, it finds the pair in its bucket's chain the same way and removes it from the chain. No other bucket is affected.

As long as the chains stay short, every operation only looks at a few pairs. If most keys pile into one bucket, that chain grows long, and the table becomes as slow as a plain list.

## Real-life analogy
Mail slots in an apartment building, one per floor. Every letter goes into the slot for its floor, and to find your letter, you only look through the pile for your floor.

## When to use it
- You don't know how many keys you'll store, since chains can always grow.
- You delete often. Removing a pair from a chain is simple and leaves the rest of the table alone.
- The table is often quite full.

## When to avoid it
- Memory is tight. Every pair in a chain needs extra room, and chains are scattered around memory, which is slower for the computer to read.

## In PyDSA
- You choose the number of buckets, and the table can hold more keys than it has buckets.
- The display shows every bucket with its chain, so keys that collided sit side by side.
