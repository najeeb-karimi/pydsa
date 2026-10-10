# LRU Cache
> An LRU cache keeps a limited number of key-value pairs and remembers which were used most recently. When a new key needs room, it removes the least recently used entry.

## What it is
LRU means least recently used. A cache holds values you want to reuse instead of fetching or computing them again. It has a capacity and an eviction rule for when all its slots are occupied.

## How it works
A hash table maps each key to a doubly linked node. The list runs from most recent at its head to least recent at its tail. Knowing a node directly lets the cache unlink it without searching the list.

Get finds a key and moves its node to the head. A missing key leaves the cache unchanged. Put replaces an existing value and moves that key to the head. For a new key at capacity, Put removes the tail from both the list and the table, then adds the new entry at the head. Replacing a key does not evict another key.

## Real-life analogy
Imagine a small desk holding reference books. Each time you use one, place it nearest your hand. When you bring a new book to a full desk, return the book you have ignored longest to the shelf.

## When to use it
Use it to explore bounded caches for repeated lookups, such as recently opened documents or computed results. Recent use is useful when recently accessed entries are likely to be needed again.

## When to avoid it
If every request is for a new key, the cache has little chance to help. LRU measures recency, not frequency or age in seconds. This learning cache has no expiration timer, persistence or concurrent access support.

## In PyDSA
Choose a capacity from 1 to 50, load the three-entry example or generate random key-value pairs. The core accepts any positive integer capacity and hashable keys; floating-point keys must be finite. Get raises a missing-key error in the core and a friendly message on screen. Put returns the evicted pair, if any. The key table is drawn beside the most-to-least-recent list, or above it when the terminal is narrow. Evictions and recency changes are narrated. Guides, code views, quizzes and fresh predictions are available. The implementation reuses the chaining hash table, doubly linked list and nodes already in PyDSA.
