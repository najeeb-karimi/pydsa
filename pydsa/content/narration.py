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
    "select": "{value} is the next one in order, so it was placed at index {index}.",
    "ordered": "This pass needed no swaps, so the list is already in order.",
    "insert": "{value} slid to the left into index {index}, past every value that belongs after it.",
    "in_place": "{value} already came after the values before it, so it stayed at index {index}.",
    "partition": "The pivot {pivot} landed at index {index}: between indexes {low} and {high}, values that "
                 "belong before it sit to its left, and those that belong after it sit to its right.",
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

    # Red-black and multi-key search trees
    "tree_found": "Found {key} in this node.",
    "tree_missing": "The search reached an empty branch without finding {key}.",
    "tree_walk": "Visited {key}; the traversal has collected {keys}.",
    "rb_insert": "Added {key} as a red leaf; now check its parent and the root.",
    "rb_remove": "Removed one occurrence of {key}; now repair any lost black height.",
    "rb_successor": "The inorder successor {successor} moves into {key}'s position, preserving search order.",
    "rb_recolor": "Colored {key} {color}.",
    "rb_rotate": "Rotated {direction} at {node}, putting {top} above it while keeping search order.",
    "rb_insert_uncle": "The parent and uncle are red, so recolor them black and move the check up from {node}.",
    "rb_insert_inner": "The new key forms an inner bend at {node}; rotate its parent to make a straight path.",
    "rb_insert_outer": "The path through {node} is straight and the uncle is black; recolor and rotate the grandparent.",
    "rb_delete_red_sibling": "The sibling under {node} is red; recolor and rotate to expose a black sibling.",
    "rb_delete_black_children": "The sibling under {node} has two black children; recolor it red and move the missing black up.",
    "rb_delete_near": "The sibling {node} has a red near child and a black far child; rotate to put red on the far side.",
    "rb_delete_far": "The sibling under {node} has a red far child; recolor and rotate to restore black height.",
    "bt_visit": "Compare {key} with the sorted keys in this node: {keys}.",
    "bt_descend": "Follow child {index}, the next range that can hold {key}.",
    "bt_split": "Split a full node and lift its middle key {key} into the parent.",
    "bt_insert": "Inserted {key} into its sorted position in a leaf.",
    "bt_borrow_left": "Move separator {key} down and borrow the left sibling's largest key to replace it.",
    "bt_borrow_right": "Move separator {key} down and borrow the right sibling's smallest key to replace it.",
    "bt_merge": "Join two minimum-size siblings with separator {key} to make one node.",
    "bt_replace": "Replace internal key {key} with neighboring key {value}, then remove that copy further down.",
    "bt_remove": "Removed one copy of {key} from its leaf.",
    "bt_done": "Deletion of {key} is complete; the root has been shortened or cleared if needed.",

    # Hash tables
    "home": "{key} hashes to index {index}, where the work starts.",
    "update": "{key} was already there, so only its value changed.",
    "chain": "Added the pair to the end of the chain in bucket {index}.",
    "chain_probe": "Pair {position} in bucket {index} holds {key}, which isn't {target}, so the search continues along the chain.",
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
    "place": "Placed {vertex} next in the order.",
    "edge_removed": "The in-degree of {v} fell to {degree} after removing the edge from {u}.",
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
    sentence = template.format(**{key: _written(key, value, label) for key, value in event.data.items()})
    if event.kind in {"match", "passed", "too_small", "too_large", "block", "bound"} and "low" in event.data:
        sentence += f" Active range: low {event.data['low']}, high {event.data['high']}."
        if "mid" in event.data:
            sentence += f" Mid: {event.data['mid']}."
    if "comparisons" in event.data:
        sentence += (f" Work since the previous step: {event.data['comparisons']} comparisons "
                     f"and {event.data['writes']} writes.")
    return sentence


def _written(key, value, label):
    """Return one value of a step's data as it should read in the sentence."""
    if key == "color":
        return "red" if value == "R" else "black"
    if key == "keys":
        return ", ".join(label(item) for item in value)
    if key in VALUE_KEYS:
        return label(value)  # A value is written as a whole, even when it's a tuple, like a queue entry
    if isinstance(value, (list, tuple)):
        return ", ".join(str(item) for item in value)
    return str(value)
