import pytest

from module8.collection import OrderedCollection
from module8.linked_list import LinkedList
from module8.queue import Queue
from module8.stack import Stack


@pytest.fixture(params=[LinkedList, Stack, Queue])
def collection(request) -> OrderedCollection[int]:
    return request.param()


def test_add_first(collection):
    collection.add_first(1)
    _verify(collection, 1)

    collection.add_first(2)
    _verify(collection, 2, 1)

    collection.add_first(3)
    _verify(collection, 3, 2, 1)


def test_add_last(collection):
    collection.add_last(1)
    _verify(collection, 1)

    collection.add_last(2)
    _verify(collection, 1, 2)

    collection.add_last(3)
    _verify(collection, 1, 2, 3)


def test_remove_first(collection):
    collection.add_last(1)
    collection.add_last(2)
    collection.add_last(3)
    _verify(collection, 1, 2, 3)

    assert collection.remove_first() == 1
    _verify(collection, 2, 3)

    assert collection.remove_first() == 2
    _verify(collection, 3)

    assert collection.remove_first() == 3
    _verify(collection)

    with pytest.raises(IndexError):
        collection.remove_first()


def test_remove_last(collection):
    collection.add_last(1)
    collection.add_last(2)
    collection.add_last(3)
    _verify(collection, 1, 2, 3)

    assert collection.remove_last() == 3
    _verify(collection, 1, 2)

    assert collection.remove_last() == 2
    _verify(collection, 1)

    assert collection.remove_last() == 1
    _verify(collection)

    with pytest.raises(IndexError):
        collection.remove_last()


def _verify_list(s, expected):
    # verify __length__
    assert len(s) == len(expected)

    # verify __contains__
    for item in expected:
        assert item in s

    # verify __iter__
    for item in iter(s):
        assert item in expected


def _verify(s, *expected):
    _verify_list(s, list(expected))
