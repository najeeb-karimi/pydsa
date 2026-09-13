"""Rich renderers for the intro, definitions, explanations and every data structure.

User data always goes into Text objects, so brackets in a value are never read as rich markup.
"""

from rich import box
from rich.cells import cell_len
from rich.columns import Columns
from rich.measure import Measurement
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.tree import Tree

from pydsa import __version__
from pydsa.content import texts
from pydsa.ui.console import console, info, plural, result

STRIKE = chr(0x0336)  # Combining long stroke overlay


def fmt(value):
    """Show a value the way Python writes it, so the str '7' and the int 7 look different."""
    return repr(value)


def strike(text):
    """Return text with every character struck out; unlike a color, this stays visible in piped output."""
    return "".join(char + STRIKE for char in text)


def plain_output():
    """Return True when colors aren't shown (piped output, NO_COLOR or a terminal without colors).

    Highlights then need a text marker instead of a style.
    """
    return console.no_color or console.color_system is None


def show(renderable, **options):
    """Print a blank line, then the renderable."""
    console.print()
    console.print(renderable, **options)


def note(text):
    """Print a dimmed explanatory line, usually right below a table."""
    console.print(Text(text, style="muted"))


def _panel(text, title, style="info"):
    return Panel(Text(text), title=title, title_align="left", border_style=style, padding=(0, 1))


def _table(title=None, **options):
    return Table(title=title, title_justify="left", title_style="title", header_style="muted", **options)


def _fits(table):
    """Return True if table fits the terminal at the width it really needs."""
    # Measure without the terminal's width limit, which would otherwise squeeze the table to fit
    return Measurement.get(console, console.options.update(width=10_000), table).maximum <= console.width


# ---------------------------------------------------------------------------
# Intro, definitions and explanations
# ---------------------------------------------------------------------------

def ascii_art(art):
    """Print an ASCII title exactly as drawn, without wrapping it to the terminal width."""
    show(Text(art.strip("\n"), style="accent"), soft_wrap=True)


def main_intro():
    """Show the PyDSA banner, the welcome panel with version and changelog, and the overview."""
    ascii_art(texts.BANNER)
    about = Text(texts.WELCOME)
    about.append(f"\n\n⏳ Version {__version__}\n", style="title")
    about.append(texts.CHANGELOG)
    about.append("\n\n")
    about.append(texts.SOURCE_CODE)
    show(Panel(about, title="💻 PyDSA", title_align="left", border_style="accent", padding=(0, 1)))
    show(_panel(texts.OVERVIEW, "🏗️ Data Structures and Algorithms"))


def intro(art, definition_text, *tables):
    """Show a data structure's ASCII title, definition and complexity tables."""
    ascii_art(art)
    definition(definition_text, *tables)


def definition(text, *tables):
    """Show a definition in a panel, followed by its complexity tables."""
    show(_panel(text, "🎯 Definition"))
    for table in tables:
        complexity(table)


def explanation(title, text):
    """Show an algorithm explanation or a longer note in a panel."""
    show(_panel(text, f"ℹ️ {title}"))


def complexity(table):
    """Show a ComplexityTable and its note."""
    grid = _table(f"⏱️ {table.title}", box=box.SIMPLE_HEAVY)
    for position, column in enumerate(table.columns):
        grid.add_column(column, style="code" if position else None)
    for row in table.rows:
        grid.add_row(*row)
    show(grid)
    if table.note:
        note(table.note)


def goodbye():
    """Say goodbye when the user exits."""
    show(Text("👋 Thanks for learning with PyDSA. Goodbye!", style="accent"))


# ---------------------------------------------------------------------------
# Arrays, stacks, queues and deques
# ---------------------------------------------------------------------------

def _slots(cells, markers=None):
    """Return a table with one column per slot, or one row per slot if that's too wide for the terminal.

    cells holds a Text per slot and markers an optional label per slot (such as "front").
    """
    wide = Table(box=box.SQUARE, header_style="muted", show_footer=markers is not None, footer_style="accent")
    for index in range(len(cells)):
        wide.add_column(str(index), footer=markers[index] if markers else "", justify="center", no_wrap=True)
    wide.add_row(*cells)
    if _fits(wide):
        return wide

    tall = Table(box=box.SQUARE, header_style="muted")
    tall.add_column("Index", justify="right", style="muted")
    tall.add_column("Value")
    if markers is not None:
        tall.add_column("", style="accent")
    for index, cell in enumerate(cells):
        tall.add_row(str(index), cell, *([markers[index]] if markers is not None else []))
    return tall


def array(items):
    """Show an array as a row of indexed cells."""
    show(_slots([Text(fmt(item)) for item in items]))


def stack(stack):
    """Show a stack from the top down, marking the top item and summarizing unused slots."""
    size = len(stack)
    empty = stack.capacity - size
    table = Table(box=box.SQUARE, header_style="muted")
    table.add_column("Index", justify="right", style="muted")
    table.add_column("Item", justify="center", min_width=9)
    table.add_column("", style="accent")
    if empty > 3:
        table.add_row(f"{size}–{stack.capacity - 1}", Text(f"{empty} empty slots", style="muted"), "")
    else:
        for index in range(stack.capacity - 1, size - 1, -1):
            table.add_row(str(index), Text("empty", style="muted"), "")
    for index in range(size - 1, -1, -1):
        table.add_row(str(index), Text(fmt(stack.items[index])), "← top" if index == size - 1 else "")
    show(table)


def circular_slots(buffer, ends):
    """Show every slot of a circular array (a queue or deque) with markers for its ends.

    ends maps a marker name, such as "front", to the slot it marks. Items that were already removed
    but not yet overwritten are struck out.
    """
    cells, markers = [], []
    leftovers = False
    for index, slot in enumerate(buffer.slots):
        if buffer.is_live(index):
            cells.append(Text(fmt(slot)))
        elif slot is None:
            cells.append(Text("empty", style="muted"))
        else:
            leftovers = True
            cells.append(Text(strike(fmt(slot)), style="muted"))
        names = [] if buffer.is_empty() else [name for name, at in ends.items() if at == index]
        markers.append("/".join(names))
    show(_slots(cells, markers))
    if leftovers:
        note("Struck-out items were already removed; their slots are free to reuse.")


def sorting_steps(items, steps):
    """Show items before sorting and after every step from a sorting generator; return the number of steps.

    Values that changed since the previous step are highlighted, and marked with * when colors aren't shown.
    """
    marker = "*" if plain_output() else ""
    table = _table("🪜 Sorting steps", box=box.SIMPLE_HEAVY)
    table.add_column("Step", justify="right", style="muted")
    table.add_column("Array")
    previous = list(items)
    table.add_row("start", _values(previous))
    count = 0
    for count, step in enumerate(steps, start=1):
        changed = {index for index, (old, new) in enumerate(zip(previous, step)) if old != new}
        table.add_row(str(count), _values(step, changed, marker))
        previous = step
    show(table)
    if marker:
        note("* marks the values that moved in each step.")
    return count


def _values(values, changed=(), marker=""):
    """Return a list of values as Text, highlighting the positions in changed."""
    text = Text("[")
    for index, value in enumerate(values):
        if index:
            text.append(", ")
        if index in changed:
            text.append(fmt(value) + marker, style="changed")
        else:
            text.append(fmt(value))
    text.append("]")
    return text


# ---------------------------------------------------------------------------
# Linked lists
# ---------------------------------------------------------------------------

def _node(label):
    """Return the three lines of a boxed node."""
    bar = "─" * (cell_len(label) + 2)
    return (
        Text(f"┌{bar}┐", style="code"),
        Text.assemble(("│ ", "code"), label, (" │", "code")),
        Text(f"└{bar}┘", style="code"),
    )


def _link(arrow):
    """Return the three lines of an arrow between nodes, drawn on the middle line."""
    padding = " " * cell_len(arrow)
    return Text(padding), Text(arrow, style="accent"), Text(padding)


def linked_list(items, doubly=False, circular=False, backward=False):
    """Show linked list items as boxed nodes joined by arrows, wrapping onto more rows when needed.

    A circular list ends with an arrow back to where the reading started; backward means the items run
    from the tail to the head.
    """
    if not items:
        info("The list is empty.")
        return

    arrow = " ⇄ " if doubly else " → "
    pieces = [_link("None ← ")] if doubly and not circular else []
    for position, item in enumerate(items):
        if position:
            pieces.append(_link(arrow))
        pieces.append(_node(fmt(item)))
    if circular:
        pieces.append(_link(f"{arrow}back to the {'tail' if backward else 'head'}"))
    else:
        pieces.append(_link(" → None"))

    rows, width = [[]], 0
    for piece in pieces:
        piece_width = cell_len(piece[1].plain)
        if rows[-1] and width + piece_width > console.width:
            rows.append([])
            width = 0
        rows[-1].append(piece)
        width += piece_width

    console.print()
    for row in rows:
        for line in range(3):
            console.print(Text.assemble(*(piece[line] for piece in row)), soft_wrap=True)
    if backward:
        note("Read from the tail back to the head by following the prev links.")
    else:
        loop = ", and the tail links back to the head" if circular else ""
        note(f"{plural(len(items), 'node')}, from the head on the left to the tail on the right{loop}.")


# ---------------------------------------------------------------------------
# Trees
# ---------------------------------------------------------------------------

def binary_tree(tree):
    """Show a binary tree with each child labeled L (left) or R (right)."""
    if tree.root is None:
        info("The tree is empty.")
        return
    view = Tree(Text.assemble(("root ", "muted"), fmt(tree.root.key)), guide_style="muted")
    _add_children(view, tree.root)
    show(view)


def _add_children(branch, node):
    for side, child in (("L", node.left), ("R", node.right)):
        if child is not None:
            _add_children(branch.add(Text.assemble((f"{side} ", "muted"), fmt(child.key))), child)


def traversal(name, keys):
    """Show the keys visited by a tree traversal."""
    result(f"{name} traversal: {', '.join(fmt(key) for key in keys) or 'the tree is empty'}")


# ---------------------------------------------------------------------------
# Graphs
# ---------------------------------------------------------------------------

def adjacency_matrix(matrix):
    """Show an adjacency matrix as a grid with the vertex numbers along both edges."""
    if not matrix:
        info("The graph has no vertices.")
        return
    table = _table("Adjacency Matrix", box=box.SQUARE)
    table.add_column(Text("from \\ to"), justify="right", style="muted")
    for vertex in range(len(matrix)):
        table.add_column(str(vertex), justify="right")
    for vertex, row in enumerate(matrix):
        table.add_row(str(vertex), *(Text(str(weight), style="muted" if weight == 0 else "code") for weight in row))
    show(table)
    note("Rows are the source vertex and columns the destination; 0 means no edge.")


def adjacency_list(adj_list):
    """Show each vertex with its outgoing edges."""
    if not adj_list:
        info("The graph has no vertices yet.")
        return
    table = _table("Adjacency List", box=box.SQUARE)
    table.add_column("Vertex", justify="right", style="code")
    table.add_column("Edges")
    for vertex, edges in adj_list.items():
        cell = Text("   ".join(f"→ {neighbor} ({weight})" for neighbor, weight in edges)) if edges else Text("no edges", style="muted")
        table.add_row(str(vertex), cell)
    show(table)
    note("Each edge is shown as → neighbor (weight).")


# ---------------------------------------------------------------------------
# Hash tables and hash sets
# ---------------------------------------------------------------------------

def chaining_table(table):
    """Show every bucket of a separate chaining hash table with its chain of key-value pairs."""
    grid = _table("Separate Chaining Hash Table", box=box.SQUARE)
    grid.add_column("Bucket", justify="right", style="code")
    grid.add_column("Chain")
    for index, bucket in enumerate(table.table):
        chain = " → ".join(f"{fmt(key)}: {fmt(value)}" for key, value in bucket)
        grid.add_row(str(index), Text(chain) if bucket else Text("empty", style="muted"))
    show(grid)


def probing_table(table):
    """Show every slot of a linear probing hash table, including the slot each key hashes to."""
    grid = _table("Linear Probing Hash Table", box=box.SQUARE)
    grid.add_column("Slot", justify="right", style="code")
    grid.add_column("Key")
    grid.add_column("Value")
    grid.add_column("Home slot", justify="right", style="muted")
    for index, slot in enumerate(table.table):
        if slot is None:
            grid.add_row(str(index), Text("empty", style="muted"), "", "")
        else:
            key, value = slot
            grid.add_row(str(index), Text(fmt(key)), Text(fmt(value)), str(table.hash_function(key)))
    show(grid)
    note("The home slot is where a key's hash points; a key that collided sits further along.")


def set_items(items):
    """Return items in set notation, with numbers before strings and each group sorted."""
    ordered = sorted(items, key=lambda item: (isinstance(item, str), item))
    return "{" + ", ".join(fmt(item) for item in ordered) + "}" if ordered else "∅ (the empty set)"


def hash_sets(sets):
    """Show the buckets of each named hash set side by side, then every set in set notation."""
    tables = []
    for name, hash_set in sets.items():
        grid = _table(f"Set {name}", box=box.SQUARE)
        grid.add_column("Bucket", justify="right", style="code")
        grid.add_column("Items")
        for index, bucket in enumerate(hash_set.table.table):
            chain = " → ".join(fmt(item) for item, _ in bucket)
            grid.add_row(str(index), Text(chain) if bucket else Text("empty", style="muted"))
        tables.append(grid)
    show(Columns(tables, padding=(0, 4)))
    for name, hash_set in sets.items():
        note(f"{name} = {set_items(hash_set)}")


# ---------------------------------------------------------------------------
# Disjoint sets
# ---------------------------------------------------------------------------

def disjoint_set(union_find):
    """Show the parent and rank arrays of a disjoint set, then the sets they describe."""
    title = "Parent and Rank Arrays"
    table = _table(title, box=box.SQUARE)
    table.add_column("Element", justify="right", style="muted")
    for element in range(len(union_find)):
        table.add_column(str(element), justify="center")
    table.add_row("Parent", *(Text(str(parent), style="code" if parent == element else "")
                              for element, parent in enumerate(union_find.parent)))
    table.add_row("Rank", *(str(rank) for rank in union_find.rank))

    if not _fits(table):
        table = _table(title, box=box.SQUARE)
        for column in ("Element", "Parent", "Rank"):
            table.add_column(column, justify="right")
        for element, (parent, rank) in enumerate(zip(union_find.parent, union_find.rank)):
            table.add_row(str(element), Text(str(parent), style="code" if parent == element else ""), str(rank))

    show(table)
    note("A root is its own parent, and a root's rank is an upper bound on the height of its tree.")
    disjoint_sets(union_find)


def disjoint_sets(union_find):
    """Show every set of a disjoint set with its root and members."""
    groups = union_find.groups()
    table = _table(plural(len(groups), "set").capitalize(), box=box.SQUARE)
    table.add_column("Root", justify="right", style="code")
    table.add_column("Members")
    table.add_column("Size", justify="right", style="muted")
    for root in sorted(groups):
        members = groups[root]
        table.add_row(str(root), Text("{" + ", ".join(str(member) for member in members) + "}"), str(len(members)))
    show(table)
