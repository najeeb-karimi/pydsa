"""A* and its zero-heuristic Dijkstra comparison on a four-neighbor, unit-cost grid."""

from dataclasses import dataclass
from heapq import heappop, heappush
from itertools import count
from typing import NamedTuple

from pydsa.algorithms.trace import record


@dataclass(frozen=True)
class Grid:
    """Rows and columns are positive; cells are zero-based (row, column) tuples."""

    rows: int
    columns: int
    walls: frozenset = frozenset()

    def __post_init__(self):
        if any(type(size) is not int or size < 1 for size in (self.rows, self.columns)):
            raise ValueError("Grid dimensions must be positive integers.")
        object.__setattr__(self, "walls", frozenset(self.walls))
        for cell in self.walls:
            self.check(cell)

    def check(self, cell):
        if (not isinstance(cell, tuple) or len(cell) != 2
                or any(type(value) is not int for value in cell)
                or not (0 <= cell[0] < self.rows and 0 <= cell[1] < self.columns)):
            raise ValueError("A cell must be a (row, column) tuple inside the grid.")

    def neighbors(self, cell):
        row, column = cell
        for other in ((row - 1, column), (row, column + 1), (row + 1, column), (row, column - 1)):
            if (0 <= other[0] < self.rows and 0 <= other[1] < self.columns
                    and other not in self.walls):
                yield other


def manhattan(cell, goal):
    return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])


class GridPath(NamedTuple):
    path: list | None
    expanded: list


def a_star(grid, start, goal, trace=None, *, heuristic=manhattan):
    """Return a shortest path and expanded cells; heuristic=None runs Dijkstra.

    A supplied heuristic must be non-negative, consistent and zero at the goal.
    Ties prefer smaller remaining estimates, then insertion order. Trace snapshots
    copy the frontier, closed cells and the route to the current cell.
    """
    for cell in (start, goal):
        grid.check(cell)
        if cell in grid.walls:
            raise ValueError("Start and goal must be open cells.")
    estimate = (lambda cell: 0) if heuristic is None else lambda cell: heuristic(cell, goal)
    serial = count()
    frontier, closed, expanded = {start}, set(), []
    costs, previous = {start: 0}, {}
    heap = [(estimate(start), estimate(start), next(serial), 0, start)]

    def route(cell):
        path = [cell]
        while path[-1] != start:
            path.append(previous[path[-1]])
        return path[::-1]

    while heap:
        _, _, _, cost, current = heappop(heap)
        if current in closed or cost != costs[current]:
            continue
        frontier.remove(current)
        closed.add(current)
        expanded.append(current)
        if current != goal:
            for neighbor in grid.neighbors(current):
                if neighbor not in closed and cost + 1 < costs.get(neighbor, float("inf")):
                    costs[neighbor], previous[neighbor] = cost + 1, current
                    remaining = estimate(neighbor)
                    heappush(heap, (cost + 1 + remaining, remaining, next(serial), cost + 1, neighbor))
                    frontier.add(neighbor)
        if trace is not None:
            record(trace, "grid_goal" if current == goal else "grid_expand",
                   (frozenset(frontier), frozenset(closed), tuple(route(current))),
                   cell=current, distance=cost, estimate=estimate(current), opened=len(frontier))
        if current == goal:
            return GridPath(route(current), expanded)
    record(trace, "grid_unreachable", (frozenset(), frozenset(closed), ()), goal=goal)
    return GridPath(None, expanded)
