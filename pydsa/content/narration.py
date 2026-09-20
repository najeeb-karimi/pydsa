"""One caption per kind of step, so the code that does the work never spells out any wording.

Every TraceEvent from pydsa.algorithms.trace names a kind, and TEMPLATES has one sentence per kind, with
the event's data filled into its {placeholders}. caption() writes that sentence; the values the user typed
are written the way the rest of PyDSA writes them.
"""

# The data keys that hold a value from the structure, which is written with the caller's label function
VALUE_KEYS = frozenset({"a", "b", "value", "pivot", "key", "target", "node", "successor",
                        "child", "parent", "word", "prefix", "char", "root", "top", "item"})

TEMPLATES = {
    # Sorting
    "swap": "{a} came after {b}, so the two swapped places.",
    "select": "{value} is the next one in order, so it moved to index {index}.",
    "insert": "{value} slid to the left into index {index}, past every value that belongs after it.",
    "in_place": "{value} already came after the values before it, so it stayed at index {index}.",
    "partition": "The pivot {pivot} landed at index {index}: from {low} on, the smaller values sit before it "
                 "and the larger ones after it, up to {high}.",
    "sift": "Sifted the value at index {index} down until everything below it followed the heap rule.",
    "take_root": "The root held {value}, the next value in order, so it moved to index {index}, just outside the heap.",
    "gap": "Put every two values that sit {gap} apart in order.",
    "merge": "Merged the two sorted halves between indexes {low} and {high} into one sorted part.",
    "count_write": "Wrote every copy of {value} into the next free indexes, straight from its counter.",
    "digit": "Sorted by the digit in the {place}s place, keeping the order from the round before.",

    # Searching
    "match": "Index {index} holds {value}, which is what you were looking for.",
    "passed": "Index {index} holds {value}, which isn't the target, so the search moves on.",
    "too_small": "{value} at index {index} is smaller than {target}, so the target can only sit further right.",
    "too_large": "{value} at index {index} is larger than {target}, so the target can only sit further left.",
    "block": "This block ends with {value} at index {index}, which isn't smaller than {target}, "
             "so the target can only be inside the block.",
    "bound": "{value} at index {index} is already past {target}, so the target can only sit before it.",

    # Heaps
    "add_leaf": "Added {value} as the last leaf, at index {index}.",
    "move_last": "Took the root {root} out and moved the last leaf, {value}, up to the root.",
    "replace": "Index {index} holds {value} now.",
    "unordered": "Started from the keys in the order they came in.",
    "sift_up": "{value} belongs above {parent}, so the two swapped places.",
    "sift_down": "{value} belongs below {child}, so the two swapped places.",

    # Binary search trees
    "empty_tree": "The tree was empty, so {key} becomes its root.",
    "go_left": "{key} is smaller than {node}, so the walk goes left.",
    "go_right": "{key} isn't smaller than {node}, so the walk goes right.",
    "place_left": "{node} has no left child, so {key} becomes one.",
    "place_right": "{node} has no right child, so {key} becomes one.",
    "delete_leaf": "{key} has no children, so it's simply cut off.",
    "delete_one_child": "{key} has one child, {child}, which takes its place.",
    "successor": "{key} has two children, so its in-order successor {successor} takes its place "
                 "and is deleted further down.",
    "unbalanced": "Node {node} is out of balance by {balance}, so its subtree has to be rotated.",
    "rotate": "The {case} rotation put {top} on top, and the subtree is balanced again.",

    # Hash tables
    "home": "{key} hashes to index {index}, where the work starts.",
    "update": "{key} was already there, so only its value changed.",
    "chain": "Added the pair to the end of the chain in bucket {index}.",
    "found": "Index {index} holds {key}.",
    "miss": "{key} isn't in the table.",
    "remove": "Took {key} out of index {index}.",
    "probe": "Slot {index} is taken by {key}, so the search probes the next slot.",
    "free": "Slot {index} is free, so the pair goes there.",
    "full": "Every slot is taken, so there's no room for {key}.",
    "rehash": "Put {key} back in, so the gap left behind can't hide it; it landed in slot {index}.",

    # Disjoint sets
    "hop": "{element} points at {parent}, so the walk moves up to it.",
    "root": "{element} is its own parent, so it's the root of its set.",
    "compress": "Pointed {element} straight at the root {root}, which shortens the walk next time.",
    "same_set": "{a} and {b} already share the root {root}, so nothing changes.",
    "attach": "The tree of {child} isn't the taller one, so it hangs under {parent}.",
    "rank_up": "Both trees were the same height, so the rank of {root} goes up by one.",

    # Tries
    "follow": "There's already a link for {char}, so the walk follows it to {prefix}.",
    "new_node": "There was no link for {char}, so a new node for {prefix} was added.",
    "mark_word": "Marked the node at the end of {word} as a word.",
    "no_link": "There's no link for {char}, so nothing spells {prefix}.",
    "is_word": "The node at the end is marked, so {word} really is a word here.",
    "not_word": "The node at the end isn't marked, so {word} is only the start of other words.",
    "unmark": "Took the word mark off the node at the end of {word}.",
    "prune": "Nothing leads through {prefix} to a word any more, so that node was pruned.",
    "keep_node": "The node for {prefix} still leads to a word, so the pruning stops here.",

    # Graph traversals
    "visit": "Visited {vertex}.",
    "enqueue": "The neighbors of {vertex} that haven't been seen yet line up behind it: {neighbors}.",
    "back": "Every neighbor of {vertex} has been seen, so the search steps back.",

    # Dijkstra's shortest paths
    "settle": "{vertex} came off the heap at a distance of {distance}, which is as short as it gets.",
    "stale": "{vertex} was already reached by a shorter path, so this heap entry is skipped.",
    "relax": "Going through {through} reaches {vertex} in {distance}, which is shorter than anything so far.",

    # Topological sort
    "no_incoming": "No edge points at these vertices, so they can go first: {vertices}.",
    "place": "Placed {vertex} next in the order and took its edges away.",
    "ready": "Nothing points at {vertex} any more, so it lines up next.",
    "cycle_left": "Edges still point at these vertices, so they sit on a cycle or after one: {vertices}.",

    # Cycle detection
    "enter": "Stepped into {vertex}, which is on the current path now.",
    "leave": "Left {vertex}, because no edge leads from there back into the path.",
    "cycle_edge": "The edge from {u} back to {v} closes a cycle, because {v} is on the current path.",
    "join": "{u} and {v} were in different groups, so this edge joins them.",
    "cycle_link": "{u} and {v} are connected already, so this edge closes a cycle.",

    # Minimum spanning trees
    "start_tree": "Started a new tree at {vertex}.",
    "accept": "Took the edge {u} — {v} with weight {weight} into the tree.",
    "skip": "Left the edge {u} — {v} out, because it would close a cycle.",
}


def caption(event, label=repr):
    """Return the sentence for a step; label writes the values it mentions, such as keys or queue entries.

    Raises KeyError if the kind has no template, and the event's data must hold every value its template asks
    for. Lists are written as "1, 2, 3".
    """
    template = TEMPLATES[event.kind]
    return template.format(**{key: _written(key, value, label) for key, value in event.data.items()})


def _written(key, value, label):
    """Return one value of a step's data as it should read in the sentence."""
    if key in VALUE_KEYS:
        return label(value)  # A value is written as a whole, even when it's a tuple, like a queue entry
    if isinstance(value, (list, tuple)):
        return ", ".join(str(item) for item in value)
    return str(value)
