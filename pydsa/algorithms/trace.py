"""The step events that data structures and algorithms record while they work.

An operation that can be watched step by step takes a trace list and appends one TraceEvent per step to it;
called without a trace, it does the same work and records nothing. Sorting generators yield their events
instead, one per step.

Nothing here decides how a step is worded or drawn: content/narration.py turns an event into a sentence,
and ui/render.py draws its snapshot.
"""

from types import MappingProxyType
from typing import Any, NamedTuple

EMPTY = MappingProxyType({})  # Shared by every event without marks or data, and never changed


class TraceEvent(NamedTuple):
    """One step of an operation: what happened, the state it left behind and the values to talk about."""

    kind: str  # What happened, such as "swap" or "probe"; content/narration.py has one caption per kind
    snapshot: Any = None  # A copy of the state to draw: a list, a tree as nested tuples, a table or a queue
    marks: Any = EMPTY  # Position or key -> the part it plays in this step, such as {3: "moved"}
    data: Any = EMPTY  # The values the caption needs, such as {"a": 5, "b": 2}


def event(kind, snapshot=None, marks=None, **data):
    """Return a TraceEvent; the data is passed as keyword arguments, as in event("swap", items, a=5, b=2)."""
    return TraceEvent(kind, snapshot, marks or EMPTY, data or EMPTY)


def record(trace, kind, snapshot=None, marks=None, **data):
    """Add an event to trace, or do nothing when the caller didn't ask for the steps."""
    if trace is not None:
        trace.append(event(kind, snapshot, marks, **data))


def tree(node, replacing=None, replacement=None):
    """Copy a subtree as nested tuples, optionally replacing one node before its link is reconnected."""
    if node is None:
        return None
    if node is replacing:
        return tree(replacement)
    return node.key, tree(node.left, replacing, replacement), tree(node.right, replacing, replacement)
