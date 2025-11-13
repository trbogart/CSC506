import pytest

from queue import Queue

value1 = "value1"
value2 = "value2"
value3 = "value3"

def test_empty():
    queue = Queue()
    _verify_elements(queue)

def test_push():
    queue = Queue()
    queue.push(value1)
    _verify_elements(queue, value1)
    queue.push(value2)
    _verify_elements(queue, value1, value2)

def test_peek():
    queue = Queue()

    # empty
    with pytest.raises(IndexError):
        queue.peek()
    queue.push(value1)
    assert queue.peek() == value1
    queue.push(value2)
    assert queue.peek() == value1

def test_pop():
    queue = Queue()

    # empty
    with pytest.raises(IndexError):
        queue.pop()

    queue.push(value1)

    # removes only element
    assert queue.pop() == value1
    _verify_elements(queue)

    # removes first element if multiple
    queue.push(value1)
    queue.push(value2)
    assert queue.pop() == value1
    _verify_elements(queue, value2)
    assert queue.pop() == value2
    _verify_elements(queue)

def test_index():
    queue = Queue()
    queue.push(value1)
    queue.push(value2)
    assert queue.index(value1) == 0
    assert queue.index(value2) == 1
    with pytest.raises(ValueError):
        queue.index("invalid")

def _verify_elements(queue, *expected):
    assert len(queue) == len(expected)
    expected_list = list(expected)
    assert list(iter(queue)) == expected_list
