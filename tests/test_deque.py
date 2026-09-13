"""Fixed-capacity circular deque, checked against collections.deque."""

import random
from collections import deque

import pytest

from pydsa.core.deque import Deque
from pydsa.core.errors import CapacityError, EmptyError


def test_random_operations_match_collections_deque():
    rng = random.Random(12)
    for _ in range(300):
        capacity = rng.randint(1, 6)
        dq, model = Deque(capacity), deque()
        for _ in range(50):
            op = rng.choice(["push_front", "push_back", "pop_front", "pop_back", "peek_front", "peek_back"])
            if op.startswith("push"):
                item = rng.randint(0, 99)
                if len(model) == capacity:
                    with pytest.raises(CapacityError):
                        getattr(dq, op)(item)
                else:
                    getattr(dq, op)(item)
                    (model.appendleft if op == "push_front" else model.append)(item)
            elif not model:
                with pytest.raises(EmptyError):
                    getattr(dq, op)()
            elif op == "pop_front":
                assert dq.pop_front() == model.popleft()
            elif op == "pop_back":
                assert dq.pop_back() == model.pop()
            elif op == "peek_front":
                assert dq.peek_front() == model[0]
            else:
                assert dq.peek_back() == model[-1]

            assert dq.to_list() == list(model)
            assert len(dq) == len(model)
            assert dq.is_empty() == (not model)
            assert dq.is_full() == (len(model) == capacity)
            assert sum(dq.is_live(i) for i in range(capacity)) == len(model)
            if model:
                assert dq.slots[dq.front] == model[0]
                assert dq.slots[dq.back] == model[-1]


def test_both_ends_wrap_around():
    dq = Deque(4)
    dq.push_front(1)  # The front steps back from slot 0 to the last slot
    assert dq.front == 3
    assert dq.slots == [None, None, None, 1]
    dq.push_back(2)  # The back wraps around to slot 0
    assert dq.slots == [2, None, None, 1]
    assert dq.to_list() == [1, 2]
    assert dq.pop_back() == 2
    assert dq.slots == [2, None, None, 1]  # The popped item stays in its slot until it's overwritten
    assert not dq.is_live(0)
