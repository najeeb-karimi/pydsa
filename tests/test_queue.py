"""Fixed-capacity circular queue, checked against collections.deque."""

import random
from collections import deque

import pytest

from pydsa.core.errors import CapacityError, EmptyError
from pydsa.core.queue import Queue


def test_random_operations_match_a_deque():
    rng = random.Random(5)
    for _ in range(200):
        capacity = rng.randint(1, 6)
        queue, model = Queue(capacity), deque()
        for _ in range(40):
            op = rng.choice(["enqueue", "enqueue", "dequeue", "front", "rear"])
            if op == "enqueue":
                item = rng.randint(0, 99)
                if len(model) == capacity:
                    with pytest.raises(CapacityError):
                        queue.enqueue(item)
                else:
                    queue.enqueue(item)
                    model.append(item)
            elif not model:
                with pytest.raises(EmptyError):
                    {"dequeue": queue.dequeue, "front": queue.get_front, "rear": queue.get_rear}[op]()
            elif op == "dequeue":
                assert queue.dequeue() == model.popleft()
            elif op == "front":
                assert queue.get_front() == model[0]
            else:
                assert queue.get_rear() == model[-1]
            assert queue.to_list() == list(model)
            assert len(queue) == len(model)
            assert queue.is_full() == (len(model) == capacity)
            # Exactly the slots holding queued items are live
            assert sum(queue.is_live(i) for i in range(capacity)) == len(model)


def test_dequeued_items_stay_in_their_slot_until_overwritten():
    queue = Queue(3)
    for item in (1, 2, 3):
        queue.enqueue(item)
    queue.dequeue()
    assert queue.slots == [1, 2, 3]
    assert [queue.is_live(i) for i in range(3)] == [False, True, True]
    queue.enqueue(4)
    assert queue.slots == [4, 2, 3]
    assert queue.to_list() == [2, 3, 4]
