import pytest

from sorted_list import SortedList


def test_empty():
    sorted_list = SortedList()
    _verify_elements(sorted_list)


def test_push():
    sorted_list = SortedList()
    sorted_list.push(1)
    _verify_elements(sorted_list, 1)
    sorted_list.push(3)
    _verify_elements(sorted_list, 1, 3)
    sorted_list.push(2)
    _verify_elements(sorted_list, 1, 2, 3)
    sorted_list.push(0)
    _verify_elements(sorted_list, 0, 1, 2, 3)


def test_peek():
    sorted_list = SortedList()

    # empty
    with pytest.raises(IndexError):
        sorted_list.peek()
    sorted_list.push(0)
    assert sorted_list.peek() == 0
    sorted_list.push(2)
    assert sorted_list.peek() == 2
    sorted_list.push(1)
    assert sorted_list.peek() == 2


def test_pop():
    sorted_list = SortedList()

    # empty
    with pytest.raises(IndexError):
        sorted_list.pop()

    sorted_list.push(1)

    # removes only element
    assert sorted_list.pop() == 1
    _verify_elements(sorted_list)

    # removes last element if multiple
    sorted_list.push(2)
    sorted_list.push(1)
    assert sorted_list.pop() == 2
    _verify_elements(sorted_list, 1)
    assert sorted_list.pop() == 1
    _verify_elements(sorted_list)


def test_index():
    sorted_list = SortedList()
    sorted_list.push(2)
    sorted_list.push(1)
    sorted_list.push(3)
    with pytest.raises(ValueError):
        sorted_list.index(0)
    assert sorted_list.index(1) == 0
    assert sorted_list.index(2) == 1
    assert sorted_list.index(3) == 2


def test_clear():
    sorted_list = SortedList()
    sorted_list.push(1)
    sorted_list.push(2)
    sorted_list.clear()
    _verify_elements(sorted_list)


def _verify_elements(sorted_list, *expected):
    assert len(sorted_list) == len(expected)
    expected_list = list(expected)
    assert list(iter(sorted_list)) == expected_list
