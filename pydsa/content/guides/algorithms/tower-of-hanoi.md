# Tower of Hanoi

> Move a tower between three pegs, one top disk at a time. A larger disk may never sit above a smaller disk.

## What it is
Tower of Hanoi is a recursive disk-moving puzzle with three pegs and ordered disk sizes.

## How it works
To move n disks, move n minus one to the spare peg, move the largest disk to the destination, then move the smaller tower onto it. Zero disks need no moves. The recurrence doubles the smaller tower's work and adds one, giving exactly 2^n - 1 moves.

## Real-life analogy
Temporarily move the smaller plates off a large plate, relocate the large plate, then stack the smaller plates back onto it.

## When to use it
Use it to learn recursive decomposition, a base case and exponential growth.

## When to avoid it
Avoid large disk counts for playback: even one extra disk nearly doubles the moves.

## In PyDSA
Type 0 to 10 disks, load three disks or generate a small random tower. Solve moves from A to C using B, snapshots the pegs after every move and explains the exact count. Disk labels preserve sizes in plain output. Long runs can be watched interactively or summarized.
