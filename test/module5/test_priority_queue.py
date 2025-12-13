import random

import pytest

from module5.priority_queue import PriorityQueue


def test_push_pop():
    pq = PriorityQueue()

    # initially empty
    assert len(pq) == 0
    assert len(pq.min_heap) == 0
    with pytest.raises(IndexError):
        pq.pop()
    with pytest.raises(IndexError):
        pq.peek()

    # push initial value
    pq.push('a', 10)
    assert pq.peek() == ('a', 10)
    assert len(pq) == 1
    assert repr(pq.min_heap) == "['a': 10]"

    # push lower priority
    pq.push('b', 5)
    assert pq.peek() == ('b', 5)
    assert len(pq) == 2
    assert repr(pq.min_heap) == "['b': 5, 'a': 10]"

    # push higher priority
    pq.push('c', 20)
    assert pq.peek() == ('b', 5)
    assert len(pq) == 3
    assert repr(pq.min_heap) == "['b': 5, 'a': 10, 'c': 20]"

    # push middle priority
    pq.push('d', 15)
    assert pq.peek() == ('b', 5)
    assert len(pq) == 4
    assert repr(pq.min_heap) == "['b': 5, 'a': 10, 'c': 20, 'd': 15]"

    # push lower priority
    pq.push('e', 0)
    assert len(pq) == 5
    assert repr(pq.min_heap) == "['e': 0, 'b': 5, 'c': 20, 'd': 15, 'a': 10]"
    assert pq.peek() == ('e', 0)

    # now pop
    assert pq.pop() == ('e', 0)
    assert len(pq) == 4
    assert repr(pq.min_heap) == "['b': 5, 'a': 10, 'c': 20, 'd': 15]"
    assert pq.peek() == ('b', 5)

    assert pq.pop() == ('b', 5)
    assert len(pq) == 3
    assert repr(pq.min_heap) == "['a': 10, 'd': 15, 'c': 20]"
    assert pq.peek() == ('a', 10)

    assert pq.pop() == ('a', 10)
    assert len(pq) == 2
    assert repr(pq.min_heap) == "['d': 15, 'c': 20]"
    assert pq.peek() == ('d', 15)

    assert pq.pop() == ('d', 15)
    assert len(pq) == 1
    assert repr(pq.min_heap) == "['c': 20]"
    assert pq.peek() == ('c', 20)

    assert pq.pop() == ('c', 20)
    assert len(pq) == 0
    assert repr(pq.min_heap) == '[]'

    with pytest.raises(IndexError):
        pq.pop()
    with pytest.raises(IndexError):
        pq.peek()


def test_random():
    random.seed(42)
    pq = PriorityQueue()
    expected = {}

    for value in range(1000):
        priority = random.randint(0, 100)
        expected[value] = priority
        pq.push(value, priority)

    max_priority = -1
    while len(pq) > 0:
        value, priority = pq.pop()

        # sorted by priority
        assert priority >= max_priority

        # has expected priority
        assert expected[value] == priority
        del expected[value]

        if priority > max_priority:
            max_priority = priority
    assert len(pq) == 0
