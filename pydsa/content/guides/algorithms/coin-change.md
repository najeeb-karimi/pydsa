# Coin Change

> Find the fewest coins needed for an amount, or count all unordered ways to make it. Each denomination can be reused.

## What it is
Coin change solves amounts using unlimited copies of positive integer denominations.

## How it works
Fewest Coins tries every possible last coin using already solved smaller amounts and remembers an optimal choice. Count Ways processes denominations in rows, adding combinations without the coin to combinations using it from the same row. Processing by denomination avoids counting different orders separately.

## Real-life analogy
At a cashier, ask either for the shortest handful of coins or for the number of different handfuls that pay the same bill.

## When to use it
Use it when [greedy](glossary:greedy-algorithm) largest-coin-first choices may fail or when you need the number of combinations.

## When to avoid it
Avoid this model for limited coin supplies or negative or fractional denominations; large amounts can also make its tables expensive.

## In PyDSA
Type up to 6 denominations from 1 to 30 and a target from 0 to 30, or use example or random inputs. Duplicates merge. Watch both tables and minimum-coin reconstruction. An impossible amount has no minimum and zero ways; zero needs zero coins and has one empty combination.
