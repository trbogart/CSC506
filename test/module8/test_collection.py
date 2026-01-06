import random

import pytest

from module8.collection import Collection
from module8.hash_table import HashTable
from module8.linked_list import LinkedList
from module8.set import Set
from module8.tree import BinarySearchTree


@pytest.fixture(params=[Set, HashTable, BinarySearchTree, LinkedList])
def collection(request) -> Collection:
    return request.param()


def test_empty(collection):
    _verify(collection)
    assert 1 not in collection


def test_add(collection):
    assert collection.add(1)
    _verify(collection, 1)

    assert collection.add(2)
    _verify(collection, 1, 2)


def test_clear(collection):
    collection.add(1)
    collection.add(2)
    collection.add(3)
    collection.clear()
    _verify(collection)


def test_remove(collection):
    collection.add(1)
    collection.add(2)
    collection.add(3)
    _verify(collection, 1, 2, 3)
    assert collection.remove(2)
    _verify(collection, 1, 3)
    assert not collection.remove(2)
    _verify(collection, 1, 3)
    assert collection.remove(1)
    _verify(collection, 3)
    assert collection.remove(3)
    _verify(collection)
    assert not collection.remove(3)


def test_random(collection):
    random.seed(1732)
    data = [i + 1 for i in range(100)]

    for _ in range(10):
        random.shuffle(data)
        expected = set()

        expected = []
        for item in data:
            collection.add(item)
            expected.append(item)
            _verify_list(collection, expected)

        random.shuffle(data)
        for item in data:
            collection.remove(item)
            expected.remove(item)
            _verify_list(collection, expected)

        assert len(collection) == 0


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
