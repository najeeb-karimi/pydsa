# Linear Probing Hash Table
> A linear probing hash table stores every pair directly in one of its slots. When a key's home slot is taken, it tries the next slot, then the next, until it finds a free one.

## What it is
Linear probing is a kind of open addressing, also called closed hashing: every key-value pair lives in the table's own slots, with no lists attached. Each [key](glossary:key) has a home slot, computed by the [hash function](glossary:hash-function). When a [collision](glossary:collision) sends a key to a taken slot, the key goes into the next free slot along, wrapping around to slot 0 after the last slot.

## How it works
- Inserting starts at the key's home slot and [probes](glossary:probing) forward one slot at a time. It stops at the same key, whose value it updates, or at an empty slot, where the new pair goes. Coming all the way back around means the table is full.
- Searching follows the same path. It stops when it finds the key, or at an empty slot, which means the key isn't in the table.
- Deleting needs care. Emptying a slot would break the probe path of the keys after it, so later searches would stop at the gap too early. One fix is to take out every pair that follows in the same [cluster](glossary:cluster) and insert them again, which is called [rehashing](glossary:rehashing).

Keys that collide build up runs of taken slots, called clusters. The fuller the table gets, the longer its clusters grow, and the more slots every operation has to probe.

## Real-life analogy
Parking on a street where every car has an assigned spot. If your spot is taken, you park in the next free spot along the street. To find your car later, you start at your assigned spot and walk forward until you see it, or until you reach an empty spot and know it isn't there.

## When to use it
- You know roughly how many keys you'll store and can keep the table well below full.
- Speed matters. The pairs sit side by side in one array, which computers read quickly.
- Memory is tight, since there are no chains to store.

## When to avoid it
- The table might fill up, since it can never hold more keys than it has slots.
- You delete often, since every delete has to repair the cluster after it.

## In PyDSA
- You choose the number of slots, and inserting into a full table is rejected.
- Deleting a key rehashes the rest of its cluster, and PyDSA tells you how many keys it rehashed.
- The display shows each key's home slot next to the slot it's really in, so you can see which keys had to probe.
