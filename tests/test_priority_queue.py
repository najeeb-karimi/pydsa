"""Priority queue, checked against a list sorted by priority and arrival."""

import random

import pytest

from pydsa.core.errors import EmptyError, NotFoundError
from pydsa.core.priority_queue import PriorityQueue

ITEMS = ["a", "b", "c", 3, 4.5]


def test_random_operations_match_a_sorted_model():
    rng = random.Random(18)
    for _ in range(300):
        queue, model, arrivals = PriorityQueue(), [], 0  # model holds [priority, arrival, item] lists
        for _ in range(40):
            op = rng.choices(["enqueue", "dequeue", "peek", "change"], weights=[5, 3, 1, 2])[0]
            item, priority = rng.choice(ITEMS), rng.randint(0, 5)
            if op == "enqueue":
                queue.enqueue(item, priority)
                model.append([priority, arrivals, item])
                arrivals += 1
            elif op == "dequeue":
                if model:
                    first = min(model)
                    model.remove(first)
                    assert queue.dequeue()[:2] == (first[2], first[0])
                else:
                    with pytest.raises(EmptyError):
                        queue.dequeue()
            elif op == "peek":
                if model:
                    first = min(model)
                    assert queue.peek() == (first[2], first[0])
                else:
                    with pytest.raises(EmptyError):
                        queue.peek()
            else:
                matches = [waiting for waiting in model if waiting[2] == item]
                if matches:
                    target = min(matches, key=lambda waiting: waiting[1])  # The copy that arrived first
                    old, target[0] = target[0], priority
                    assert queue.change_priority(item, priority)[0] == old
                else:
                    with pytest.raises(NotFoundError):
                        queue.change_priority(item, priority)

            assert [(waiting.priority, waiting.item) for waiting in queue.in_order()] == [
                (priority, item) for priority, _, item in sorted(model)
            ]
            assert len(queue) == len(model)


def test_equal_priorities_are_served_first_in_first_out():
    queue = PriorityQueue()
    for item in ["first", "second", "third"]:
        queue.enqueue(item, 2)
    queue.enqueue("urgent", 1)
    assert [queue.dequeue()[0] for _ in range(4)] == ["urgent", "first", "second", "third"]
    assert queue.is_empty()


def test_changing_a_priority_keeps_the_arrival_order():
    queue = PriorityQueue()
    queue.enqueue("a", 5)
    queue.enqueue("b", 1)
    queue.enqueue("c", 1)
    old, steps = queue.change_priority("a", 1)
    assert old == 5 and steps
    assert [waiting.item for waiting in queue.in_order()] == ["a", "b", "c"]

    queue.enqueue("x", 3)
    queue.enqueue("x", 3)
    queue.change_priority("x", 0)
    first, second = [waiting for waiting in queue.in_order() if waiting.item == "x"]
    assert first.priority == 0 and second.priority == 3
    assert first.order < second.order  # The copy that arrived first was changed
