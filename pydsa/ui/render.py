"""Rich renderers for the intro, guides, explanations, operation notes, code and every data structure.

User data always goes into Text objects, so brackets in a value are never read as rich markup.
"""

import inspect
import re
import textwrap

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

from pydsa import __version__, settings
from pydsa.content import complexity, notes, registry, texts
from pydsa.ui.console import console, info, page, plural, result

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
    return Table(title=title, title_justify="left", title_style="title", header_style="muted", **options)


def _fits(table):
    """Return True if table fits the terminal at the width it really needs."""
    # Measure without the terminal's width limit, which would otherwise squeeze the table to fit
    return Measurement.get(console, console.options.update(width=10_000), table).maximum <= console.width


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


def start_session():
    """Forget that the intro was shown, so the next home() shows it in full."""
    global _intro_shown
    _intro_shown = False


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
                table.add_row(topic.id, Text(topic.title) if topic.parent is None else Text.assemble(("↳ ", "muted"), topic.title))
        show(table)
    note("Open a topic directly with: pydsa --topic ID")


def _markdown_panel(text, title):
    """Return Markdown text from a guide in a panel, with its glossary links in bold."""
    return Panel(Markdown(registry.markdown(text), hyperlinks=False), title=title, title_align="left",
                 border_style="info", padding=(0, 1))


def _sections(parsed, icons):
    """Return a guide's summary and sections as one Markdown text, with an icon before each heading."""
    parts = [f"> {parsed.summary}"]
    parts += [f"## {icons.get(heading, '🔹')} {heading}\n\n{body}" for heading, body in parsed.sections]
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


def intro(art, topic_id):
    """Show a topic's ASCII title, the summary from its guide and its complexity tables."""
    ascii_art(art)
    parsed = registry.guide(topic_id)
    show(_markdown_panel(parsed.summary, f"🎯 {parsed.title}"))
    note("Choose Read the Guide in the topic's menu for the whole guide.")
    console.print(Group(*_complexity(topic_id)))


def summary(topic_id):
    """Show the summary from a topic's guide, such as the kind of tree the user just picked."""
    parsed = registry.guide(topic_id)
    show(_markdown_panel(parsed.summary, f"🧪 {parsed.title}"))


def guide(topic_id):
    """Show a topic's whole guide and its complexity tables, a screenful at a time if they're taller than the terminal."""
    parsed = registry.guide(topic_id)
    parts = [_markdown_panel(_sections(parsed, SECTION_ICONS), f"📖 {parsed.title}"), *_complexity(topic_id)]
    if registry.glossary_links(parsed.body()):
        parts.append(Text("📘 Words in bold are explained in the Glossary, under Learning Tools on the main menu.", style="muted"))
    page(Group(*parts))


def explanation(topic_id):
    """Show how an algorithm works before it runs, following the Explanations setting.

    Brief shows the summary from the algorithm's guide, and Detailed its How it works section.
    """
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
            show(Text.assemble("⏱️ ", cost_text))
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

    children(node) returns the (left, right) pair, with None for a missing child, and label(node) returns a Text.
    Every line is padded to the same width, so subtrees can be placed side by side.
    """
    text = label(node)
    size = cell_len(text.plain)
    left, right = children(node)
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


def _outline(node, children, label):
    """Return a rich Tree of the subtree rooted at node, with each child labeled L (left) or R (right)."""
    view = Tree(Text.assemble(("root ", "muted"), label(node)), guide_style="muted")
    branches = [(view, node)]
    while branches:
        branch, parent = branches.pop(0)
        for side, child in zip("LR", children(parent)):
            if child is not None:
                branches.append((branch.add(Text.assemble((f"{side} ", "muted"), label(child))), child))
    return view


def _tree(root, children, label):
    """Print a binary tree as a top-down diagram, or as an outline if the diagram is too wide for the terminal."""
    lines, _ = _diagram(root, children, label)
    console.print()
    if cell_len(lines[0].plain) <= console.width:
        for line in lines:
            line.rstrip()
            console.print(line, soft_wrap=True)
        return True
    console.print(_outline(root, children, label))
    note("The tree is too wide to draw here, so it's shown as an outline: L marks a left child and R a right child.")
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


def traversal(name, keys):
    """Show the keys visited by a tree traversal."""
    result(f"{name} traversal: {', '.join(fmt(key) for key in keys) or 'the tree is empty'}")


def tree_stats(tree, name="tree"):
    """Show the height, node count, leaf count and smallest and largest keys of a tree or heap."""
    if len(tree) == 0:
        info(f"The {name} is empty.")
        return
    table = _table("📏 Tree stats", box=box.SQUARE)
    table.add_column("Stat")
    table.add_column("Value", justify="right", style="code")
    table.add_row("Height (levels)", str(tree.height()))
    table.add_row("Nodes", str(len(tree)))
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


def heap_steps(steps, first, label=fmt):
    """Show every step of a heap operation as a tree and as the array; first describes the starting step.

    The keys that moved are highlighted, and marked with * when colors aren't shown.
    """
    marker = "*" if plain_output() else ""
    for number, step in enumerate(steps):
        if number == 0:
            caption = first
        else:
            was, went = step.moved
            direction = "up" if went < was else "down"
            relative = "parent" if went < was else "child"
            caption = f"Moved {label(step.items[went])} {direction}, swapping it with its {relative} {label(step.items[was])}."
        console.print()
        console.print(Text(f"Step {number}: {caption}", style="title"))
        if step.items:
            _heap_tree(step.items, label, step.moved, marker)
            console.print(Text.assemble(("Array: ", "muted"), _values(step.items, step.moved, marker, label)))
    if len(steps) == 1:
        note("No swaps were needed: the heap property already held.")
    elif marker:
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
    order = ", ".join(str(vertex) for vertex in paths.order)
    note(f"Every path starts at vertex {paths.source}. The distances became final in this order: {order}.")


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
