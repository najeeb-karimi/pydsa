"""Choose walls and endpoints, watch A*, and compare its work with Dijkstra."""

import random

from pydsa.algorithms.grid_search import Grid, a_star
from pydsa.content import texts
from pydsa.ui import render, stepper
from pydsa.ui.console import ask, ask_int, error, info, result
from pydsa.ui.menu import Menu, Nav, back_option, operation_menu

MAX_SIZE = 10


def run():
    while True:
        render.intro(texts.A_STAR_ASCII, "a-star")
        data = Menu("🛠️ How do you want to create the grid?", [
            [("Type walls row by row", create), ("Use the example", example),
             ("Place random walls", lambda: create(True))], [back_option()],
        ]).open()
        if data is Nav.BACK:
            return Nav.BACK
        outcome = operation_menu("grid", "a-star", operations(*data), new_label="New Grid").run()
        if outcome is not Nav.NEW:
            return outcome


def endpoint(board, name):
    while True:
        row = ask_int(f"🔢 {name} row (0–{board.rows - 1})?", "row", min_value=0, max_value=board.rows - 1)
        column = ask_int(f"🔢 {name} column (0–{board.columns - 1})?", "column",
                         min_value=0, max_value=board.columns - 1)
        if (row, column) not in board.walls:
            return row, column
        error("That cell is a wall. Choose an open cell.")


def create(random_walls=False):
    rows = ask_int("🔢 How many rows (1–10)?", "row count", min_value=1, max_value=MAX_SIZE)
    columns = ask_int("🔢 How many columns (1–10)?", "column count", min_value=1, max_value=MAX_SIZE)
    walls = set()
    if random_walls:
        walls = {(r, c) for r in range(rows) for c in range(columns) if random.random() < .3}
        # Always leave at least one open cell so an endpoint can be chosen.
        walls.discard((0, 0))
    else:
        info("Type . for an open cell and # for a wall, with no spaces.")
        for row in range(rows):
            while True:
                line = ask(f"Row {row}: {columns} cells").strip()
                if len(line) != columns or set(line) - {".", "#"}:
                    error(f"Use exactly {columns} dots or # characters.")
                    continue
                if row == rows - 1 and len(walls) + line.count("#") == rows * columns:
                    error("The grid needs at least one open cell. Change this row.")
                    continue
                walls.update((row, c) for c, char in enumerate(line) if char == "#")
                break
    board = Grid(rows, columns, walls)
    render.grid(board, None, None)
    start, goal = endpoint(board, "Start"), endpoint(board, "Goal")
    render.grid(board, start, goal)
    return board, start, goal


def example():
    board, start, goal = Grid(5, 7, {(1, 1), (1, 2), (1, 3), (2, 3), (3, 3)}), (0, 0), (4, 6)
    render.grid(board, start, goal)
    return board, start, goal


def operations(board, start, goal):
    return [("Run A*", lambda: search(board, start, goal)),
            ("Compare with Dijkstra", lambda: compare(board, start, goal)),
            ("Display", lambda: render.grid(board, start, goal))]


def search(board, start, goal):
    render.explanation("a-star")
    trace = []
    paths = a_star(board, start, goal, trace)
    draw = lambda number, event: render.grid_step(number, event, board, start, goal)
    def all_cells(events):
        for number, event in enumerate(events, 1):
            draw(number, event)
    stepper.play(trace, draw, summary=all_cells)
    if paths.path is None:
        result(f"Goal is unreachable. Expanded {len(paths.expanded)} cells.")
    else:
        result(f"Shortest path: {len(paths.path) - 1} moves. Expanded {len(paths.expanded)} cells.")


def compare(board, start, goal):
    informed = a_star(board, start, goal)
    uninformed = a_star(board, start, goal, heuristic=None)
    for name, paths in (("A* (Manhattan)", informed), ("Dijkstra (zero heuristic)", uninformed)):
        length = "unreachable" if paths.path is None else f"{len(paths.path) - 1} moves"
        result(f"{name}: {length}; expanded {len(paths.expanded)} cells.")
    saved = len(uninformed.expanded) - len(informed.expanded)
    info(f"Dijkstra expansions minus A*: {saved}. Walls and ties affect the saving; it can be zero or negative.")
