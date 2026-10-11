"""Rich renderers for the intro, guides, explanations, operation notes, code and every data structure.

User data always goes into Text objects, so brackets in a value are never read as rich markup.
"""

import inspect
import re
import textwrap
import unicodedata
from math import inf

from rich import box
from rich.cells import cell_len
from rich.columns import Columns
from rich.console import Group
from rich.markdown import Markdown
from rich.measure import Measurement
from rich.padding import Padding
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from rich.tree import Tree

from pydsa import __version__, progress, settings
from pydsa.content import complexity, narration, notes, registry, texts
from pydsa.ui.console import console, info, page, plural, result, spaced_label

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


def _table(title=None, **options):
    return Table(title=spaced_label(title) if title else title, title_justify="left", title_style="title",
                 header_style="muted", **options)


def _fits(table):
    """Return True if table fits the terminal at the width it really needs."""
    # Measure without the terminal's width limit, which would otherwise squeeze the table to fit
    return Measurement.get(console, console.options.update(width=10_000), table).maximum <= console.width


def dp_items(weights, values, capacity):
    table = _table("Knapsack items")
    for title in ("Index", "Weight", "Value"):
        table.add_column(title)
    for i, (weight, value) in enumerate(zip(weights, values)):
        table.add_row(str(i), str(weight), str(value))
    show(table)
    note(f"Capacity: {capacity}. Each item can be chosen at most once.")


def dp_table(snapshot, marks=()):
    """Draw all states and arrows, switching to wrapped row listings on narrow terminals."""
    values, rows, columns = snapshot["table"], snapshot["rows"], snapshot["columns"]
    arrows = snapshot.get("arrows")

    def entry(i, j):
        value = values[i][j]
        text = "?" if value is None else str(value)
        if arrows:
            text += arrows[i][j]
        return text + ("*" if (i, j) in marks else "")

    table = _table("DP states")
    table.add_column("Row")
    for j, label in enumerate(columns):
        table.add_column(Text(f"{j}:{label!r}"))
    for i, row in enumerate(values):
        table.add_row(Text(f"{i}:{rows[i]!r}"), *(Text(entry(i, j)) for j in range(len(row))))
    if _fits(table):
        show(table)
    else:
        show(Text("DP states · compact rows (column index:value)"))
        note("Columns: " + ", ".join(f"{j}:{label!r}" for j, label in enumerate(columns)))
        for i, row in enumerate(values):
            note(f"Row {i}:{rows[i]!r} · " + "  ".join(f"{j}:{entry(i, j)}" for j in range(len(row))))
    note("* marks the current cell; ? means unfilled or unreachable. ↖ takes a match; ↑ moves up; ← moves left.")


def dp_step(number, event):
    step_caption(number, event)
    if event.snapshot:
        dp_table(event.snapshot, event.marks)


def fibonacci_comparison(rows):
    table = _table("Fibonacci call counts")
    for title in ("Method", "Value", "Calls", "States"):
        table.add_column(title)
    for row in rows:
        table.add_row(*(Text(str(value)) for value in row))
    show(table)


def recursion_tree(events, title, kind):
    """Only called for bounded small examples; Rich wraps branches to the terminal width."""
    root = Tree(Text(title), guide_style="muted")
    nodes = {}
    for event in events:
        if event.kind != kind:
            continue
        parent = nodes.get(event.data["parent"], root)
        nodes[event.data["identifier"]] = parent.add(Text(event.data["label"]))
    show(root)


def hanoi_pegs(pegs):
    """Draw disk stacks from top to bottom, with a wrapped fallback for large disks."""
    table = _table("Tower of Hanoi · top disk first")
    for peg in "ABC":
        table.add_column(peg, justify="center")
    height = max(map(len, pegs), default=0)
    for level in range(height, 0, -1):
        table.add_row(*(Text("=" * peg[level - 1] + f" {peg[level - 1]}") if len(peg) >= level else Text("|") for peg in pegs))
    if not height:
        table.add_row("|", "|", "|")
    if _fits(table):
        show(table)
    else:
        show(Text("Tower of Hanoi · compact pegs"))
        for name, peg in zip("ABC", pegs):
            note(f"{name} top → bottom: " + repr(tuple(reversed(peg))))


def queens_board(n, columns, marks=()):
    table = _table("N-Queens board")
    table.add_column("Row")
    for column in range(n):
        table.add_column(str(column))
    for row in range(n):
        entries = [("Q" if row < len(columns) and columns[row] == column else ".") +
                   ("*" if (row, column) in marks else "") for column in range(n)]
        table.add_row(str(row), *entries)
    if _fits(table):
        show(table)
    else:
        show(Text("N-Queens board · compact rows"))
        note("Columns: " + " ".join(map(str, range(n))))
        for row in range(n):
            note(f"{row}: " + " ".join(("Q" if row < len(columns) and columns[row] == column else ".") +
                                        ("*" if (row, column) in marks else "") for column in range(n)))
    if n == 0:
        note("Empty board: one empty solution.")
    note("Q = queen; . = empty; * = current placement, removal or rejected square.")


def backtracking_step(number, event):
    step_caption(number, event)
    if event.kind == "rec_move":
        hanoi_pegs(event.snapshot)
    elif event.kind in ("rec_place", "rec_remove", "rec_reject", "rec_solution"):
        queens_board(*event.snapshot, event.marks)
    else:
        show(Text("Current permutation prefix: " + repr(event.snapshot)))


# ---------------------------------------------------------------------------
# Intro, guides and explanations
# ---------------------------------------------------------------------------

# Shown before each section of a topic guide, so the headings stand out even without colors
SECTION_ICONS = {
    "What it is": "🎯",
    "How it works": "⚙️",
    "Real-life analogy": "🌍",
    "When to use it": "✅",
    "When to avoid it": "⚠️",
    "In PyDSA": "🐍",
}

def ascii_art(art):
    """Print an ASCII title exactly as drawn, without wrapping it to the terminal width."""
    show(Text(art.strip("\n"), style="accent"), soft_wrap=True)


def main_intro():
    """Show the PyDSA banner and the welcome panel with the version and changelog."""
    ascii_art(texts.BANNER)
    about = Text(texts.WELCOME)
    about.append(f"\n\n⏳ Version {__version__}\n", style="title")
    about.append(texts.CHANGELOG)
    about.append("\n\n")
    about.append(texts.SOURCE_CODE)
    show(Panel(about, title="💻 PyDSA", title_align="left", border_style="accent", padding=(0, 1)))
    note("New to data structures and algorithms? Start with the Overview in Learning Tools, on the main menu.")


_intro_shown = False  # Whether this session already showed the full intro
_progress_notice_shown = False


def start_session():
    """Forget that the intro was shown, so the next home() shows it in full."""
    global _intro_shown, _progress_notice_shown
    _intro_shown = False
    _progress_notice_shown = False


def skip_intro():
    """Treat the intro as shown, for sessions that open a topic directly."""
    global _intro_shown
    _intro_shown = True


def home():
    """Show the full intro the first time in a session (or every time, if the Intro setting says so); otherwise a short header."""
    global _intro_shown
    if not _intro_shown or settings.current.intro == "always":
        main_intro()
        _intro_shown = True
    else:
        show(Text.assemble(("🐍 PyDSA ", "accent"), (__version__, "title"), ("  ·  type h in any menu for help", "muted")))


def topic_list(topics, categories):
    """Show the ID and title of every topic, grouped by category, for the --list-topics option."""
    for category, title in categories.items():
        table = _table(f"📚 {title}", box=box.SIMPLE_HEAVY)
        table.add_column("ID", style="code", no_wrap=True)
        table.add_column("Topic")
        for topic in topics:
            if topic.category == category:
                title = topic_label(topic.id, topic.title)
                table.add_row(topic.id, Text(title) if topic.parent is None else Text.assemble(("↳ ", "muted"), title))
        show(table)
    note("Open a topic directly with: pydsa --topic ID")


def _markdown_panel(text, title):
    """Return Markdown text from a guide in a panel, with its glossary links in bold."""
    return Panel(Markdown(registry.markdown(text), hyperlinks=False), title=spaced_label(title), title_align="left",
                 border_style="info", padding=(0, 1))


def _sections(parsed, icons):
    """Return a guide's summary and sections as one Markdown text, with an icon before each heading."""
    parts = [f"> {parsed.summary}"]
    parts += [f"## {spaced_label(icons.get(heading, '🔹') + ' ' + heading)}\n\n{body}"
              for heading, body in parsed.sections]
    return "\n\n".join(parts)


def _complexity(topic_id):
    """Return a topic's complexity tables and their notes as renderables, each table after a blank line."""
    parts = []
    for table in complexity.TOPIC_TABLES[topic_id]:
        grid = _table(f"⏱️ {table.title}", box=box.SIMPLE_HEAVY)
        for position, column in enumerate(table.columns):
            grid.add_column(column, style="code" if position else None)
        for row in table.rows:
            grid.add_row(*row)
        parts += [Text(), grid]
        if table.note:
            parts.append(Text(table.note, style="muted"))
    return parts


def _visit(topic_id):
    """Save visits where a topic is actually shown, including nested topics and algorithm guides."""
    global _progress_notice_shown
    notice = progress.visit(topic_id)
    if notice and not _progress_notice_shown:
        info(notice)
        _progress_notice_shown = True


def topic_label(topic_id, title):
    return ("✓ " if topic_id in progress.current.visited else "") + title


def progress_summary():
    show(Text(progress.summary(), style="muted"))


def intro(art, topic_id):
    """Show a topic's ASCII title, the summary from its guide and its complexity tables."""
    _visit(topic_id)
    ascii_art(art)
    parsed = registry.guide(topic_id)
    show(_markdown_panel(parsed.summary, f"🎯 {parsed.title}"))
    note("Choose Read the Guide in the topic's menu for the whole guide.")
    console.print(Group(*_complexity(topic_id)))


def summary(topic_id):
    """Show the summary from a topic's guide, such as the kind of tree the user just picked."""
    _visit(topic_id)
    parsed = registry.guide(topic_id)
    show(_markdown_panel(parsed.summary, f"🧪 {parsed.title}"))


def guide(topic_id):
    """Show a topic's whole guide and its complexity tables, a screenful at a time if they're taller than the terminal."""
    _visit(topic_id)
    parsed = registry.guide(topic_id)
    parts = [_markdown_panel(_sections(parsed, SECTION_ICONS), f"📖 {parsed.title}"), *_complexity(topic_id)]
    if registry.glossary_links(parsed.body()):
        parts.append(Text("📘 Words in bold are explained in the Glossary, under Learning Tools on the main menu.", style="muted"))
    page(Group(*parts))


def explanation(topic_id):
    """Show how an algorithm works before it runs, following the Explanations setting.

    Brief shows the summary from the algorithm's guide, and Detailed its How it works section.
    """
    _visit(topic_id)
    parsed = registry.guide(topic_id)
    title = f"ℹ️ How {parsed.title} Works"
    if settings.current.detail == "brief":
        show(_markdown_panel(parsed.summary, title))
        note("To see how it works before it runs, set Explanations to Detailed in Settings. The whole guide is in Learning Tools.")
    else:
        show(_markdown_panel(parsed.section("How it works"), title))


def _cost(note):
    """Return what an operation costs, read from its topic's complexity tables, or an empty string."""
    parts = []
    for row in note.complexity_rows:
        values = complexity.cost(note.topic, row)
        text = values[0][1] if len(values) == 1 else " · ".join(f"{column} {value}" for column, value in values)
        parts.append(text if len(note.complexity_rows) == 1 else f"{row}: {text}")
    return "; ".join(parts)


def operation_note(note):
    """Show an operation's note before it runs, following the Explanations setting.

    Brief shows one line with the summary and the cost, and Detailed adds the numbered steps. An operation that
    shows its own explanation from a guide, like a sorting algorithm, only gets its cost.
    """
    cost = _cost(note)
    cost_text = Text.assemble(("Cost: ", "title"), (cost, "code")) if cost else None
    if note.explained:
        if cost_text:
            show(Text.assemble(spaced_label("⏱️ "), cost_text))
        return
    headline = Text.assemble((f"💡 {note.operation}: ", "title"), note.summary)
    if settings.current.detail == "brief" or not note.steps:
        if cost_text:
            headline.append(" · ")
            headline.append_text(cost_text)
        show(headline)
        return
    # A grid keeps each wrapped step indented under its own text
    steps = Table.grid(padding=(0, 1))
    steps.add_column(style="muted", justify="right", no_wrap=True)
    steps.add_column()
    for number, step in enumerate(note.steps, start=1):
        steps.add_row(f"{number}.", step)
    lines = [headline, Padding(steps, (0, 0, 0, 2), expand=False)]
    if cost_text:
        lines.append(Text.assemble("  ", cost_text))
    show(Group(*lines))


def code(note):
    """Show an operation's pseudocode and the real Python source behind it, a screenful at a time."""
    parts = [Panel(Text("\n".join(note.pseudocode)), title=f"📝 Pseudocode: {note.operation}", title_align="left",
                   border_style="info", padding=(0, 1))]
    raised = []
    for reference in note.sources:
        function = notes.resolve(reference)
        lines, start = inspect.getsourcelines(function)
        source = textwrap.dedent("".join(lines)).rstrip()
        raised += [name for name in re.findall(r"raise (\w+)", source) if name not in raised]
        syntax = Syntax(source, "python", theme="ansi_dark", line_numbers=True, start_line=start, word_wrap=True,
                        background_color="default")
        path = inspect.getmodule(function).__name__.replace(".", "/") + ".py"
        parts += [Text(), Panel(syntax, title=f"🐍 {function.__qualname__}", title_align="left", subtitle=path,
                                subtitle_align="right", border_style="muted", padding=(0, 1))]
    if raised:
        extra = (f"Besides the idea in the pseudocode, the real code checks for problems and raises {' or '.join(raised)}, "
                 "which the screen turns into a friendly message.")
    else:
        extra = "The real code follows the pseudocode closely, and its comments explain the less obvious lines."
    parts += [Text(), Text(extra, style="muted")]
    page(Group(*parts))


def document(name, icon):
    """Show one of the Learning Tools documents, such as the overview, a screenful at a time."""
    parsed = registry.document(name)
    page(_markdown_panel(_sections(parsed, {}), f"{icon} {parsed.title}"))


def glossary(terms):
    """Show glossary terms and their definitions, a screenful at a time."""
    text = "\n\n".join(f"## 🔹 {term.name}\n\n{term.definition}" for term in terms)
    page(_markdown_panel(text, "📘 Glossary"))


def goodbye():
    """Say goodbye when the user exits."""
    show(Text("👋 Thanks for learning with PyDSA. Goodbye!", style="accent"))


# ---------------------------------------------------------------------------
# Steps
# ---------------------------------------------------------------------------

def _marker():
    """Return the mark that points out what changed when colors aren't shown."""
    return "*" if plain_output() else ""


def _marked(text, mark):
    """Return text highlighted when mark is set, and marked with * when colors aren't shown."""
    return Text(text + _marker(), style="changed") if mark else Text(text)


def step_caption(number, event, label=fmt):
    """Print the heading of one step: its number and the sentence for what happened."""
    console.print()
    console.print(Text(f"Step {number}: {narration.caption(event, label)}", style="title"))


def step_captions(events, label=fmt):
    """List what happened in every step, without drawing the state after each one."""
    steps = Table.grid(padding=(0, 1))
    steps.add_column(style="muted", justify="right", no_wrap=True)
    steps.add_column()
    for number, event in enumerate(events, start=1):
        steps.add_row(f"{number}.", Text(narration.caption(event, label)))
    show(Group(Text("🪜 Step by step:", style="title"), Padding(steps, (0, 0, 0, 2), expand=False)))


def list_step(number, event, label=fmt):
    """Draw one step that works on a list, such as a sorting or a searching step."""
    step_caption(number, event, label)
    console.print(Text.assemble(("List: ", "muted"), _values(event.snapshot, event.marks, _marker(), label)))


def trace_summary(events, label=fmt):
    """Show six captions of a long run with their original step numbers."""
    console.print(Text(f"Showing 6 of {len(events)} steps; the middle {len(events) - 6} are omitted.", style="muted"))
    for index in (*range(3), *range(len(events) - 3, len(events))):
        console.print(Text(f"{index + 1}. {narration.caption(events[index], label)}"))


def tree_step(number, event):
    """Draw one step of a tree operation, with the tree it left behind."""
    step_caption(number, event)
    snapshot_tree(event.snapshot, event.marks)


def snapshot_tree(snapshot, marks=()):
    """Draw a tree held as nested (key, left, right) tuples, pointing out the keys in marks."""
    if snapshot is None:
        info("The tree is empty.")
        return
    _tree(snapshot, lambda node: (node[1], node[2]), lambda node: _marked(fmt(node[0]), node[0] in marks))


def heap_step(number, event, label=fmt):
    """Draw one step of a heap operation as a tree and as the array that stores it."""
    step_caption(number, event, label)
    if event.snapshot:
        marker = _marker()
        _heap_tree(event.snapshot, label, event.marks, marker)
        console.print(Text.assemble(("Array: ", "muted"), _values(event.snapshot, event.marks, marker, label)))


def walk_step(number, event, waiting="In the queue"):
    """Draw one step of a graph traversal: the vertices visited so far and the ones still waiting."""
    step_caption(number, event)
    order = " → ".join(str(vertex) for vertex in event.snapshot["order"])
    rest = ", ".join(str(vertex) for vertex in event.snapshot["waiting"])
    console.print(Text.assemble(("Visited: ", "muted"), order or "nothing yet"))
    console.print(Text.assemble((f"{waiting}: ", "muted"), rest or "nothing"))


def path_step(number, event):
    """Draw one step of the search for a cycle in a directed graph: the path it's on."""
    step_caption(number, event)
    path = " → ".join(str(vertex) for vertex in event.snapshot)
    console.print(Text.assemble(("Current path: ", "muted"), path or "empty"))


def edges_step(number, event, collected="Edges so far"):
    """Draw one step that collects edges, such as a step of a minimum spanning tree."""
    step_caption(number, event)
    edges = ", ".join(_edge(edge) for edge in event.snapshot)
    console.print(Text.assemble((f"{collected}: ", "muted"), edges or "none yet"))


def _edge(edge):
    """Return an edge as "0 — 1", or as "0 — 1 (4)" when it comes with a weight."""
    u, v, *weight = edge
    return f"{u} — {v}" + (f" ({weight[0]})" if weight else "")


def vertex_step(number, event, title, column):
    """Draw one step that keeps a number per vertex, such as a distance or a count of edges."""
    step_caption(number, event)
    table = _table(title, box=box.SQUARE)
    table.add_column("Vertex", justify="right", style="code")
    table.add_column(column, justify="right")
    for vertex, value in event.snapshot.items():
        table.add_row(_marked(str(vertex), vertex in event.marks),
                      Text("∞", style="muted") if value == inf else Text(str(value)))
    show(table)


def prefix_step(number, event):
    """Draw one step of a trie operation: the path spelled out from the root."""
    step_caption(number, event)
    console.print(Text.assemble(("Path from the root: ", "muted"), " → ".join(event.snapshot) or "the root"))


def hash_step(number, event, draw):
    """Draw one step of a hash table operation with draw(snapshot, marks)."""
    step_caption(number, event)
    draw(event.snapshot, event.marks)


def union_step(number, event):
    """Draw one step of a disjoint set operation: the parent and rank arrays it left behind."""
    step_caption(number, event)
    parent, rank = event.snapshot
    show(parent_arrays(parent, rank, event.marks))


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


def sorting_steps(before, events):
    """Show the list as it was before sorting, then after every step, with what happened in each one.

    Values that changed in a step are highlighted, and marked with * when colors aren't shown.
    """
    marker = _marker()
    table = _table("🪜 Sorting steps", box=box.SIMPLE_HEAVY)
    table.add_column("Step", justify="right", style="muted")
    table.add_column("Array")
    table.add_column("What happened")
    table.add_row("start", _values(before), "")
    for number, event in enumerate(events, start=1):
        table.add_row(str(number), _values(event.snapshot, event.marks, marker), narration.caption(event))
    show(table)
    if marker:
        note("* marks the values that moved in each step.")


def _values(values, changed=(), marker="", label=fmt):
    """Return a list of values as Text, highlighting the positions in changed."""
    text = Text("[")
    for index, value in enumerate(values):
        if index:
            text.append(", ")
        if index in changed:
            text.append(label(value) + marker, style="changed")
        else:
            text.append(label(value))
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

GAP = 2  # Spaces between two sibling subtrees in a tree diagram


def _diagram(node, children, label):
    """Return the lines of a top-down diagram of the subtree rooted at node, and the column of the root's middle.

    children(node) returns binary child slots or any number of multi-key children; label(node) returns a Text.
    Every line is padded to the same width, so subtrees can be placed side by side.
    """
    text = label(node)
    size = cell_len(text.plain)
    branches = tuple(children(node))
    if len(branches) != 2:
        return _multi_diagram(node, branches, children, label)
    left, right = branches
    if left is None and right is None:
        return [text], (size - 1) // 2

    # A missing child still takes up one column, so a lone child hangs clearly to its side
    left_lines, left_mid = _diagram(left, children, label) if left is not None else ([Text(" ")], 0)
    right_lines, right_mid = _diagram(right, children, label) if right is not None else ([Text(" ")], 0)
    left_width, right_width = cell_len(left_lines[0].plain), cell_len(right_lines[0].plain)
    right_mid += left_width + GAP
    mid = (left_mid + right_mid) // 2
    start = mid - (size - 1) // 2
    shift = max(0, -start)  # Move the children right if the label would stick out on the left
    start, mid, left_mid, right_mid = start + shift, mid + shift, left_mid + shift, right_mid + shift
    width = max(shift + left_width + GAP + right_width, start + size)

    connector = [" "] * width
    if left is not None:
        connector[left_mid:mid] = "┌" + "─" * (mid - left_mid - 1)
    if right is not None:
        connector[mid + 1:right_mid + 1] = "─" * (right_mid - mid - 1) + "┐"
    connector[mid] = "┴" if left is not None and right is not None else "┘" if left is not None else "└"

    lines = [
        Text.assemble(" " * start, text, " " * (width - start - size)),
        Text("".join(connector), style="muted"),
    ]
    for row in range(max(len(left_lines), len(right_lines))):
        lines.append(Text.assemble(
            " " * shift,
            left_lines[row] if row < len(left_lines) else " " * left_width,
            " " * GAP,
            right_lines[row] if row < len(right_lines) else " " * right_width,
            " " * (width - shift - left_width - GAP - right_width),
        ))
    return lines, mid


def _multi_diagram(node, branches, children, label):
    """Lay out any number of children under a multi-key node, preserving rich labels."""
    text = label(node)
    if not branches:
        return [text], (cell_len(text.plain) - 1) // 2
    diagrams = [_diagram(child, children, label) for child in branches]
    widths = [cell_len(lines[0].plain) for lines, _ in diagrams]
    offsets, offset = [], 0
    for width in widths:
        offsets.append(offset)
        offset += width + GAP
    centers = [start + mid for start, (_, mid) in zip(offsets, diagrams)]
    mid = (centers[0] + centers[-1]) // 2
    start = mid - (cell_len(text.plain) - 1) // 2
    shift = max(0, -start)
    start, mid = start + shift, mid + shift
    centers = [center + shift for center in centers]
    width = max(offset - GAP + shift, start + cell_len(text.plain))
    connector = [" "] * width
    for column in range(centers[0], centers[-1] + 1):
        connector[column] = "─"
    for index, center in enumerate(centers):
        connector[center] = "┌" if index == 0 else "┐" if index == len(centers) - 1 else "┬"
    connector[mid] = "┼" if mid in centers else "┴"
    lines = [Text.assemble(" " * start, text, " " * (width - start - cell_len(text.plain))),
             Text("".join(connector), style="muted")]
    for row in range(max(len(lines) for lines, _ in diagrams)):
        pieces = [" " * shift]
        for index, (child_lines, _) in enumerate(diagrams):
            if index:
                pieces.append(" " * GAP)
            pieces.append(child_lines[row] if row < len(child_lines) else " " * widths[index])
        pieces.append(" " * (width - (offset - GAP + shift)))
        lines.append(Text.assemble(*pieces))
    return lines, mid


def _outline(node, children, label, multi=False):
    """Return an outline with binary sides or numbered children for multi-key nodes."""
    view = Tree(Text.assemble(("root ", "muted"), label(node)), guide_style="muted")
    branches = [(view, node)]
    while branches:
        branch, parent = branches.pop(0)
        child_nodes = tuple(children(parent))
        sides = (str(index) for index in range(len(child_nodes))) if multi else "LR"
        for side, child in zip(sides, child_nodes):
            if child is not None:
                branches.append((branch.add(Text.assemble((f"{side} ", "muted"), label(child))), child))
    return view


def _tree(root, children, label, multi=False):
    """Print a tree top-down, or as an outline if the diagram is too wide for the terminal."""
    lines, _ = _diagram(root, children, label)
    console.print()
    if cell_len(lines[0].plain) <= console.width:
        for line in lines:
            line.rstrip()
            console.print(line, soft_wrap=True)
        return True
    console.print(_outline(root, children, label, multi))
    note("The tree is too wide to draw here, so it's shown as an outline: " +
         ("children are numbered from left to right." if multi else "L marks a left child and R a right child."))
    return False


def binary_tree(tree, balance=False):
    """Show a binary search tree top-down; balance adds each node's balance factor (for AVL trees)."""
    if tree.root is None:
        info("The tree is empty.")
        return

    def label(node):
        text = Text(fmt(node.key))
        if balance:
            factor = tree.balance_factor(node)
            text.append(f" ({factor:+d})" if factor else " (0)", style="muted")
        return text

    _tree(tree.root, lambda node: (node.left, node.right), label)
    if balance:
        note("In parentheses is each node's balance factor: its left height minus its right height.")


def lru_snapshot(state, marks=()):
    """Draw the existing chaining table beside the doubly linked recency order."""
    buckets, entries, capacity = state
    table = _table("Key table (bucket → node)", box=box.SQUARE)
    table.add_column("Bucket", style="muted")
    table.add_column("Key")
    table.add_column("Value")
    for index, bucket in enumerate(buckets):
        for key, value in bucket:
            table.add_row(str(index), _marked(fmt(key), key in marks), Text(fmt(value)))
    chain = Text()
    for index, (key, value) in enumerate(entries):
        if index:
            chain.append(" ↔ ", style="muted")
        chain.append_text(_marked(f"{fmt(key)}: {fmt(value)}", key in marks))
    if not entries:
        chain.append("empty", style="muted")
    recency = Panel(chain, title="Most → least recent", title_align="left", expand=False)
    together = Table.grid(padding=(0, 2))
    together.add_row(table, recency)
    show(together if _fits(together) else Group(table, Text(), recency))
    note(f"{len(entries)} of {capacity} entries. The table points to list nodes; the tail is evicted first.")


def lru_cache(cache):
    lru_snapshot(cache.snapshot())


def lru_step(number, event):
    step_caption(number, event)
    lru_snapshot(event.snapshot, event.marks)


def skip_snapshot(state, marks=()):
    """Align express lanes over base nodes, switching to one lane per wrapped row when wide."""
    rows, lanes = state
    labels = {identity: fmt(key) for identity, key, _ in rows}
    wide = Table.grid(padding=(0, 1))
    for level in range(len(lanes) - 1, -1, -1):
        lane = set(lanes[level])
        cells = [Text(f"L{level + 1}", style="muted"), _marked("HEAD", 0 in marks)]
        cells.extend(_marked(labels[identity] if identity in lane else "─", identity in marks)
                     for identity, _, _ in rows)
        cells.append(Text("END", style="muted"))
        wide.add_row(*cells)
    if _fits(wide):
        show(wide)
    else:
        table = _table("Skip-list express lanes", box=box.SQUARE)
        table.add_column("Level", style="muted")
        table.add_column("Forward links")
        for level in range(len(lanes) - 1, -1, -1):
            text = _marked("HEAD", 0 in marks)
            for identity in lanes[level]:
                text.append(" → ", style="muted")
                text.append_text(_marked(labels[identity], identity in marks))
            text.append(" → END", style="muted")
            table.add_row(str(level + 1), text)
        show(table)
        note("The lanes are too wide to align here, so each row lists its forward links.")


def skip_list(linked):
    skip_snapshot(linked.snapshot())
    note(f"Seed {linked.seed}; fair coin, heads promotes and tails stops; maximum {linked.max_level} levels. "
         "Level 1 holds every key, including duplicates.")


def skip_step(number, event):
    step_caption(number, event)
    skip_snapshot(event.snapshot, event.marks)


def bloom_snapshot(state, marks=()):
    bits, m, k, additions = state
    # Fixed-size chunks remain compact even for hundreds of bits in a narrow terminal.
    table = _table("Bloom-filter bits", box=box.SQUARE)
    table.add_column("Indexes", style="muted")
    table.add_column("Bits")
    chunk = max(4, min(32, console.width - 20))
    for start in range(0, m, chunk):
        line = Text()
        for i in range(start, min(start + chunk, m)):
            line.append_text(_marked(str(bits[i]), i in marks))
        table.add_row(f"{start}–{min(start + chunk, m) - 1}", line)
    show(table)
    note(f"m = {m} bits; k = {k} salted SHA-256 hashes; {additions} Add calls. A 1 means a bit is set, not that an item is proved present.")


def bloom_filter(bloom):
    bloom_snapshot(bloom.snapshot())


def bloom_step(number, event):
    step_caption(number, event)
    bloom_snapshot(event.snapshot, event.marks)


def bloom_experiment(experiment, rows, mode):
    table = _table(experiment.name, box=box.SIMPLE_HEAVY)
    table.add_column("Added", justify="right")
    table.add_column("False hits", justify="right")
    table.add_column("Measured", justify="right")
    table.add_column("Formula", justify="right")
    for row in rows:
        table.add_row(str(row.n), f"{row.false_positives}/{row.trials}", f"{row.measured:.1%}", f"{row.expected:.1%}")
    show(table)
    note(experiment.note)
    note("Formula: (1 - exp(-k × n / m))^k. It is an approximation for distinct items and independent uniform hashes; measured rates vary.")


def segment_snapshot(state, marks=()):
    """Show every segment's inclusive array range and aggregate, with explicit overlap marks."""
    if state is None:
        info("The tree is empty.")
        return

    def label(node):
        value = "pending" if node[2] is None else fmt(node[2])
        text = f"[{node[0]}, {node[1]}] {value}"
        mark = marks.get((node[0], node[1])) if marks else None
        if mark:
            text += f" ({mark})"
        return _marked(text, mark)

    _tree(state, lambda node: (node[3], node[4]), label)


def segment_tree(tree):
    from pydsa.core.segment_tree import snapshot
    array(tree.items)
    segment_snapshot(snapshot(tree.root))
    note(f"Each node shows [start, end] and its {tree.operation}; both ends are included.")


def segment_step(number, event):
    step_caption(number, event)
    segment_snapshot(event.snapshot, event.marks)


def fenwick_snapshot(state, marks=()):
    """Draw one-based blocks beside the zero-based array ranges they sum."""
    values, blocks = state
    array(values)
    table = _table("Fenwick blocks (one-based)", box=box.SQUARE)
    table.add_column("i / binary", style="code")
    table.add_column("Array range")
    table.add_column("Low bit")
    table.add_column("Sum", justify="right")
    width = max(1, (len(values) + 1).bit_length())
    for i in range(1, len(blocks)):
        bit = i & -i
        table.add_row(_marked(f"{i} / {i:0{width}b}", i in marks),
                      f"[{i - bit}, {i - 1}]", f"{bit:0{width}b}", Text(fmt(blocks[i])))
    show(table)


def fenwick_tree(tree):
    fenwick_snapshot((tree.items, tree.blocks))
    note("Block i covers i & -i values. Prefix queries subtract that bit; updates add it. Array indexes start at 0.")


def fenwick_step(number, event):
    step_caption(number, event)
    fenwick_snapshot(event.snapshot, event.marks)


def traversal(name, keys):
    """Show the keys visited by a tree traversal."""
    result(f"{name} traversal: {', '.join(fmt(key) for key in keys) or 'the tree is empty'}")


def red_black_snapshot(state, marks=()):
    if state is None:
        info("The tree is empty.")
        return

    def label(node):
        style = "bold red" if node[1] == "R" else "bold black on white"
        text = Text(f"{fmt(node[0])} ({node[1]})", style=style)
        if node[0] in marks:
            text.append(_marker(), style="changed")
        return text

    _tree(state, lambda node: (node[2], node[3]), label)


def red_black_tree(tree):
    from pydsa.core.red_black_tree import snapshot
    red_black_snapshot(snapshot(tree.root))
    note("R is red and B is black; missing children also count as black.")


def red_black_step(number, event):
    step_caption(number, event)
    red_black_snapshot(event.snapshot, event.marks)


def b_tree_snapshot(state, marks=()):
    if state is None:
        info("The tree is empty.")
        return

    def label(node):
        pieces = ["["]
        for index, key in enumerate(node[0]):
            if index:
                pieces.append(" | ")
            pieces.append(_marked(fmt(key), key in marks))
        return Text.assemble(*pieces, "]")

    _tree(state, lambda node: node[1], label, multi=True)


def b_tree(tree):
    from pydsa.core.b_tree import snapshot
    b_tree_snapshot(snapshot(tree.root))
    note(f"Minimum degree t = {tree.t}; each node holds at most {2 * tree.t - 1} keys.")


def b_tree_step(number, event):
    step_caption(number, event)
    b_tree_snapshot(event.snapshot, event.marks)


def tree_stats(tree, name="tree"):
    """Show the height, node count, leaf count and smallest and largest keys of a tree or heap."""
    if len(tree) == 0:
        info(f"The {name} is empty.")
        return
    table = _table("📏 Tree stats", box=box.SQUARE)
    table.add_column("Stat")
    table.add_column("Value", justify="right", style="code")
    table.add_row("Height (levels)", str(tree.height()))
    if hasattr(tree, "node_count"):
        table.add_row("Keys", str(len(tree)))
        table.add_row("Nodes", str(tree.node_count()))
        table.add_row("Minimum degree", str(tree.t))
    else:
        table.add_row("Nodes", str(len(tree)))
    if hasattr(tree, "black_height"):
        table.add_row("Black height (includes absent leaf)", str(tree.black_height()))
    table.add_row("Leaves", str(tree.leaf_count()))
    table.add_row("Smallest key", Text(fmt(tree.min())))
    table.add_row("Largest key", Text(fmt(tree.max())))
    show(table)
    note("The height counts levels of nodes; counting edges on the longest path gives one less.")


# ---------------------------------------------------------------------------
# Heaps and priority queues
# ---------------------------------------------------------------------------

def entry(entry):
    """Return a priority queue entry as "priority: item"."""
    return f"{entry.priority}: {fmt(entry.item)}"


def _heap_tree(items, label, moved=(), marker=""):
    """Print a heap's array as a tree, where index i has its children at 2i + 1 and 2i + 2."""

    def children(index):
        return tuple(child if child < len(items) else None for child in (2 * index + 1, 2 * index + 2))

    def node_label(index):
        if index in moved:
            return Text(label(items[index]) + marker, style="changed")
        return Text(label(items[index]))

    _tree(0, children, node_label)


def heap(heap, label=fmt, name="heap"):
    """Show a heap as a tree and as the array that stores it."""
    if heap.is_empty():
        info(f"The {name} is empty.")
        return
    _heap_tree(heap.items, label)
    show(_slots([Text(label(item)) for item in heap.items]))
    note("The array stores the tree level by level: index i has its children at 2i + 1 and 2i + 2.")


def heap_steps(events, label=fmt):
    """Show every step of a heap operation as a tree and as the array.

    The keys that moved are highlighted, and marked with * when colors aren't shown.
    """
    for number, event in enumerate(events, start=1):
        heap_step(number, event, label)
    if len(events) == 1:
        note("No swaps were needed: the heap rule already held.")
    elif _marker():
        note("* marks the keys that moved in each step.")


def priority_queue(queue):
    """Show a priority queue's heap and the order its items will be served in."""
    if queue.is_empty():
        info("The priority queue is empty.")
        return
    _heap_tree(queue.heap.items, entry)
    table = _table("Serving order", box=box.SQUARE)
    table.add_column("#", justify="right", style="muted")
    table.add_column("Priority", justify="right", style="code")
    table.add_column("Item")
    for position, waiting in enumerate(queue.in_order(), start=1):
        table.add_row(str(position), str(waiting.priority), Text(fmt(waiting.item)))
    show(table)
    note("Each node shows priority: item. Smaller numbers go first; ties go in arrival order.")


# ---------------------------------------------------------------------------
# Tries
# ---------------------------------------------------------------------------

def trie(trie):
    """Show a trie as a tree of characters, marking the nodes that end a word."""
    if len(trie) == 0:
        info("The trie is empty.")
        return
    view = Tree(Text("root", style="muted"), guide_style="muted")
    _add_trie_children(view, trie.root, "")
    show(view)
    note(f"✓ marks a node that ends a word. {plural(len(trie), 'word')} in {plural(trie.node_count(), 'node')}, not counting the root.")


def _add_trie_children(branch, node, spelled):
    """Add the children of a trie node to branch in character order, spelling out the words they end."""
    for char in sorted(node.children):
        child = node.children[char]
        text = Text(char, style="code")
        if child.is_word:
            text.append(f"  ✓ {fmt(spelled + char)}", style="success")
        _add_trie_children(branch.add(text), child, spelled + char)


# ---------------------------------------------------------------------------
# Graphs
# ---------------------------------------------------------------------------

def adjacency_matrix(matrix, directed=True):
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
    if directed:
        note("Rows are the source vertex and columns the destination; 0 means no edge.")
    else:
        note("The matrix is symmetric, because every undirected edge is stored both ways; 0 means no edge.")


def adjacency_list(adj_list, directed=True):
    """Show each vertex with its edges."""
    if not adj_list:
        info("The graph has no vertices yet.")
        return
    arrow = "→" if directed else "—"
    table = _table("Adjacency List", box=box.SQUARE)
    table.add_column("Vertex", justify="right", style="code")
    table.add_column("Edges")
    for vertex, edges in adj_list.items():
        cell = Text("   ".join(f"{arrow} {neighbor} ({weight})" for neighbor, weight in edges)) if edges else Text("no edges", style="muted")
        table.add_row(str(vertex), cell)
    show(table)
    if directed:
        note("Each edge is shown as → neighbor (weight).")
    else:
        note("Each edge is shown as — neighbor (weight), under both of its vertices.")


# ---------------------------------------------------------------------------
# Hash tables and hash sets
# ---------------------------------------------------------------------------

def chaining_buckets(buckets, marks=()):
    """Show every bucket of a separate chaining hash table with its chain of key-value pairs."""
    grid = _table("Separate Chaining Hash Table", box=box.SQUARE)
    grid.add_column("Bucket", justify="right", style="code")
    grid.add_column("Chain")
    for index, bucket in enumerate(buckets):
        chain = " → ".join(f"{fmt(key)}: {fmt(value)}" for key, value in bucket)
        grid.add_row(_marked(str(index), index in marks), Text(chain) if bucket else Text("empty", style="muted"))
    show(grid)


def chaining_table(table):
    """Show a separate chaining hash table as it is now."""
    chaining_buckets(table.table)


def probing_slots(slots, home, marks=()):
    """Show every slot of a linear probing hash table; home(key) gives the slot a key hashes to."""
    grid = _table("Linear Probing Hash Table", box=box.SQUARE)
    grid.add_column("Slot", justify="right", style="code")
    grid.add_column("Key")
    grid.add_column("Value")
    grid.add_column("Home slot", justify="right", style="muted")
    for index, slot in enumerate(slots):
        if slot is None:
            grid.add_row(_marked(str(index), index in marks), Text("empty", style="muted"), "", "")
        else:
            key, value = slot
            grid.add_row(_marked(str(index), index in marks), Text(fmt(key)), Text(fmt(value)), str(home(key)))
    show(grid)
    note("The home slot is where a key's hash points; a key that collided sits further along.")


def probing_table(table):
    """Show a linear probing hash table as it is now."""
    probing_slots(table.table, table.hash_function)


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

def parent_arrays(parents, ranks, marks=()):
    """Return the parent and rank arrays of a disjoint set as a table, pointing out the elements in marks."""
    title = "Parent and Rank Arrays"
    table = _table(title, box=box.SQUARE)
    table.add_column("Element", justify="right", style="muted")
    for element in range(len(parents)):
        table.add_column(_marked(str(element), element in marks), justify="center")
    table.add_row("Parent", *(Text(str(parent), style="code" if parent == element else "")
                              for element, parent in enumerate(parents)))
    table.add_row("Rank", *(str(rank) for rank in ranks))
    if _fits(table):
        return table

    table = _table(title, box=box.SQUARE)
    for column in ("Element", "Parent", "Rank"):
        table.add_column(column, justify="right")
    for element, (parent, rank) in enumerate(zip(parents, ranks)):
        table.add_row(_marked(str(element), element in marks),
                      Text(str(parent), style="code" if parent == element else ""), str(rank))
    return table


def disjoint_set(union_find):
    """Show the parent and rank arrays of a disjoint set, then the sets they describe."""
    show(parent_arrays(union_find.parent, union_find.rank))
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


# ---------------------------------------------------------------------------
# Algorithms
# ---------------------------------------------------------------------------

def sort_comparison(results):
    """Show how much work every sorting algorithm did on the same list.

    results holds (name, stats, steps) tuples, with stats None for an algorithm that can't sort the list.
    """
    table = _table("📊 Sorting algorithms compared", box=box.SQUARE)
    table.add_column("Algorithm")
    for column in ("Comparisons", "Writes", "Steps"):
        table.add_column(column, justify="right", style="code")
    rejected = False
    for name, stats, steps in results:
        if stats is None:
            rejected = True
            table.add_row(Text(name, style="muted"), *(Text("—", style="muted") for _ in range(3)))
        else:
            table.add_row(name, str(stats.comparisons), str(stats.writes), str(steps))
    show(table)
    note("Comparisons count how often two values were compared, and writes how often a value was stored in the list "
         "(a swap is two writes). Steps are the rows each algorithm shows when it runs on its own.")
    note("Try a sorted list, a reversed one and one full of duplicates to see how differently the algorithms react.")
    if rejected:
        note("— marks an algorithm that can't sort this list.")


def experiment(experiment, rows, mode):
    """Show work growth or measured false-positive rates in a narrow terminal."""
    if experiment.kind == "bloom-rate":
        bloom_experiment(experiment, rows, mode)
        return
    table = _table(f"📈 {experiment.name} ({mode})", box=box.SIMPLE_HEAVY)
    for name in ("n", "Work", "Ratio", "ms", "Growth"):
        table.add_column(name, justify="left" if name == "Growth" else "right")
    maximum = max((row.work for row in rows), default=1) or 1
    bar_width = min(12, max(1, console.width // 6))
    for row in rows:
        length = max(1, round(bar_width * row.work / maximum)) if row.work else 0
        table.add_row(str(row.n), str(row.work), f"{row.ratio:.2f}", f"{row.milliseconds:.2f}", "█" * length)
    show(table)
    note(f"Ratio = work ÷ expected(n), using {experiment.growth}. A steady ratio suggests that the measured "
         "work follows this growth pattern; it does not prove a complexity bound.")
    note(experiment.note)
    note("Milliseconds measure only the run, excluding input construction. Machine speed, tracing and allocation "
         "affect timing, so compare work counts first.")


def search_probes(values, probes, caption):
    """Show values with the order in which a search checked each position written under it."""
    markers = [
        ",".join(str(number) for number, position in enumerate(probes, start=1) if position == index)
        for index in range(len(values))
    ]
    show(_slots([Text(fmt(value)) for value in values], markers))
    note(caption)


def shortest_paths(paths, routes):
    """Show the distance and shortest path from the source to every vertex; routes maps each vertex to its path or None."""
    table = _table("🧭 Shortest paths", box=box.SQUARE)
    table.add_column("To", justify="right", style="code")
    table.add_column("Distance", justify="right")
    table.add_column("Path")
    for vertex, route in routes.items():
        if route is None:
            table.add_row(str(vertex), Text("∞", style="muted"), Text("unreachable", style="muted"))
        else:
            table.add_row(str(vertex), str(paths.distances[vertex]), " → ".join(str(step) for step in route))
    show(table)
    caption = f"Every path starts at vertex {paths.source}."
    if paths.order:
        order = ", ".join(str(vertex) for vertex in paths.order)
        caption += f" The distances became final in this order: {order}."
    note(caption)


def distance_matrix(distances, marks=None, *, negative_diagonal=False):
    """Draw all pairs, falling back to a pair table when the matrix is too wide."""
    marks = marks or {}
    table = _table("All-pairs distances", box=box.SQUARE)
    table.add_column("From / To")
    vertices = list(distances)
    for vertex in vertices:
        table.add_column(str(vertex), justify="right")
    def value(u, v):
        distance = distances[u][v]
        return _marked("∞" if distance == float("inf") else str(distance), marks.get((u, v)))
    for u in vertices:
        table.add_row(str(u), *(value(u, v) for v in vertices))
    if not _fits(table):
        table = _table("All-pairs distances", box=box.SQUARE)
        for column in ("From", "To", "Distance"):
            table.add_column(column)
        for u in vertices:
            for v in vertices:
                table.add_row(str(u), str(v), value(u, v))
    show(table)
    if marks:
        message = "Highlighted diagonal entries are negative" if negative_diagonal else "Highlighted cells improved in this pass"
        note(message + "; * marks them when colors are off.")


def floyd_step(number, event):
    step_caption(number, event)
    distance_matrix(event.snapshot, event.marks, negative_diagonal=event.kind == "floyd_cycle")


def grid(grid, start, goal, snapshot=None):
    """Draw a grid with symbolic open/closed/path markers that also work without colors."""
    opened, closed, path = snapshot or ((), (), ())
    path = set(path)
    lines = []
    for row in range(grid.rows):
        line = Text()
        for column in range(grid.columns):
            cell = row, column
            symbol, style = ".", "muted"
            if cell in grid.walls:
                symbol = "#"
            elif cell in path:
                symbol, style = "*", "changed"
            elif cell in opened:
                symbol, style = "o", "info"
            elif cell in closed:
                symbol, style = "x", "muted"
            if cell == start:
                symbol, style = "S", "success"
            if cell == goal:
                symbol, style = "G" if goal != start else "B", "result"
            line.append(symbol, style)
        lines.append(line)
    # The interactive screen caps dimensions at 10; Rich wraps wider caller-provided grids.
    show(Group(*lines))
    note("S start · G goal · B both · # wall · . unseen · o open · x closed · * current path")


def grid_step(number, event, board, start, goal):
    step_caption(number, event)
    grid(board, start, goal, event.snapshot)


def _string_character(character):
    """Keep spaces and control/combining characters visible without changing their indexes."""
    if character == " ":
        return "·"
    if not character.isprintable() or unicodedata.combining(character):
        return ascii(character)[1:-1]
    return character


def string_alignment(text, pattern, start=0, marks=None):
    """Draw the pattern under the text in fixed-width cells, splitting long alignments by index."""
    marks = marks or {}
    extent = max(len(text), start + len(pattern))
    if not extent:
        show(Text("Text: ''\nPattern: ''"))
        return
    labels = [_string_character(char) for char in text + pattern]
    width = max([len(str(extent - 1)), *(cell_len(label) for label in labels)]) + 1
    per_line = max(1, (console.width - 8) // width)
    if extent > per_line:
        show(Text("Alignment split by character index to fit the terminal.", style="muted"))
    for low in range(0, extent, per_line):
        high = min(extent, low + per_line)
        lines = []
        for name in ("Index", "Text", "Pattern", "Marks"):
            line = Text(f"{name:<8}")
            for i in range(low, high):
                j = i - start
                mark = marks.get(j) if 0 <= j < len(pattern) else None
                if name == "Index":
                    label = str(i)
                elif name == "Text":
                    label = _string_character(text[i]) if i < len(text) else ""
                elif name == "Pattern":
                    label = _string_character(pattern[j]) if 0 <= j < len(pattern) else ""
                else:
                    label = "=" if mark == "matched" else "!" if mark == "mismatch" else ""
                style = "changed" if mark and name in ("Text", "Pattern") else "muted" if name == "Index" else ""
                line.append(label + " " * (width - cell_len(label)), style)
            lines.append(line)
        show(Group(*lines))
    note("= matching character · ! mismatch · · space. Indexes count Python characters; no case folding is applied.")


def string_data(text, pattern):
    string_alignment(text, pattern)
    note(f"Text length: {len(text)}; pattern length: {len(pattern)}. Empty patterns match every boundary.")


def string_step(number, event):
    step_caption(number, event)
    if event.kind in ("ss_prefix_entry", "ss_prefix_fallback"):
        pattern, prefix = event.snapshot
        table = _table("KMP prefix table", box=box.SQUARE)
        for heading in ("Index", "Character", "LPS"):
            table.add_column(heading)
        # Only completed entries are displayed; zeros in unfinished slots are not final answers.
        last = event.data["index"] if event.kind == "ss_prefix_entry" else event.data["index"] - 1
        for i in range(last + 1):
            table.add_row(str(i), _string_character(pattern[i]), _marked(str(prefix[i]), event.marks.get(i)))
        show(table)
    else:
        text, pattern, start = event.snapshot
        marks = event.marks
        if event.kind == "ss_match":
            marks = dict.fromkeys(range(len(pattern)), "matched")
        string_alignment(text, pattern, start, marks)


def string_comparison(rows, modulus):
    table = _table("Character comparisons", box=box.SQUARE)
    for heading in ("Algorithm", "Search", "Prefix", "Total"):
        table.add_column(heading)
    for name, matches, stats in rows:
        table.add_row(name, str(stats.comparisons), str(stats.preprocessing), str(stats.total))
    show(table)
    for name, matches, stats in rows:
        note(f"{name}: match positions {matches}.")
    note(f"Rabin-Karp modulus: {modulus}. Search counts character equality checks; Prefix counts KMP table comparisons. Hash arithmetic is excluded, so fewer comparisons do not guarantee less elapsed time.")


def spanning_forest(forest):
    """Show the edges of a minimum spanning tree or forest in the order they were chosen, and the ones left out."""
    if forest.edges:
        # A short title, because a table's title wraps at the table's own width
        table = _table("🌲 Chosen edges", box=box.SQUARE)
        table.add_column("#", justify="right", style="muted")
        table.add_column("Edge", style="code")
        table.add_column("Weight", justify="right")
        for number, (u, v, weight) in enumerate(forest.edges, start=1):
            table.add_row(str(number), f"{u} — {v}", str(weight))
        show(table)
    else:
        info("No edges were chosen, because no edge connects two different vertices.")
    if forest.skipped:
        note("Left out, because they would close a cycle: " + ", ".join(f"{u} — {v} ({weight})" for u, v, weight in forest.skipped) + ".")
