# 0/1 Knapsack

> Choose a subset of items to maximize value within a weight limit. Each item can be chosen once.

## What it is
0/1 knapsack chooses whole items, with a [capacity](glossary:capacity) that limits their total weight.

## How it works
A row allows the first i items and a column gives remaining capacity. Compare skipping the current item with taking it plus the previous row's smaller-capacity answer. The previous row prevents item reuse. Trace backward: a changed value means take the item; ties skip it.

## Real-life analogy
Pack valuable objects for a flight, choosing which whole objects fit within the luggage allowance.

## When to use it
Use it for bounded whole-item selection with integer weights and a modest capacity.

## When to avoid it
Avoid it for divisible items, unlimited copies or enormous capacities; those need different models or techniques.

## In PyDSA
Type up to 8 positive integer weights and equally many nonnegative values, with capacity 0 to 30. Examples and random inputs are available. Solve fills every non-base cell and traces chosen zero-based item indexes. Empty items and zero capacity give value zero.
