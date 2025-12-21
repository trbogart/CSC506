import random

import pytest

from module6.tree_map import TreeMap

def test_empty():
    tree_map = TreeMap()
    _validate_map(tree_map, {})

def test_insert():
    tree_map = TreeMap()
    tree_map[5] = 'a'
    _validate_map(tree_map, {5: 'a'})

    tree_map[1] = 'b'
    _validate_map(tree_map, {1: 'b', 5: 'a'})

    tree_map[3] = 'b'
    _validate_map(tree_map, {1: 'b', 3: 'b', 5: 'a'})

def test_update():
    tree_map = TreeMap()
    tree_map[100] = 'a'
    tree_map[100] = 'b'
    _validate_map(tree_map, {100: 'b'})

def test_delete():
    tree_map = TreeMap()
    tree_map[5] = 'a'
    tree_map[1] = 'b'
    tree_map[3] = 'b'
    _validate_map(tree_map, {1: 'b', 3: 'b', 5: 'a'})

    del tree_map[5]
    _validate_map(tree_map, {1: 'b', 3: 'b'})
    del tree_map[1]
    _validate_map(tree_map, {3: 'b'})
    del tree_map[3]
    _validate_map(tree_map, {})

    with pytest.raises(KeyError):
        del tree_map[0]

def test_get():
    tree_map = TreeMap()
    tree_map[5] = 'a'
    tree_map[1] = 'b'
    tree_map[3] = 'b'

    assert tree_map[5] == 'a'
    assert tree_map[1] == 'b'
    assert tree_map[3] == 'b'

    with pytest.raises(KeyError):
        _ = tree_map[0]
    with pytest.raises(KeyError):
        _ = tree_map[2]
    with pytest.raises(KeyError):
        _ = tree_map[4]
    with pytest.raises(KeyError):
        _ = tree_map[6]

def test_random():
    random.seed(32342)
    tree_map = TreeMap()
    expected = {}
    num_elements = 100
    keys = [i for i in range(num_elements)]
    random.shuffle(keys)

    # insert
    for i, key in enumerate(keys):
        value = str(i)
        tree_map[key] = value
        expected[key] = value
        assert tree_map[key] == value
        assert len(tree_map) == i + 1
    _validate_map(tree_map, expected)

    # update
    random.shuffle(keys)
    for key in keys:
        value = random.randint(1, 100)
        tree_map[key] = value
        expected[key] = value
        assert len(tree_map) == num_elements
        assert tree_map[key] == value
    _validate_map(tree_map, expected)

    # delete
    random.shuffle(keys)
    for i, key in enumerate(keys):
        del tree_map[key]
        assert key not in tree_map
        assert len(tree_map) == num_elements - i - 1

    # empty
    _validate_map(tree_map, {})

def test_clear():
    tree_map = TreeMap()
    tree_map[0] = 0
    tree_map[1] = 0
    tree_map[2] = 0
    tree_map.clear()
    _validate_map(tree_map, {})

def _validate_map(tree_map, expected):
    assert len(tree_map) == len(expected)

    for key, value in expected.items():
        assert key in tree_map
        assert tree_map[key] == value

    sorted_keys = list(sorted(expected.keys()))
    assert list(tree_map.keys()) == sorted_keys

    last_key = None
    for key, value in tree_map.items():
        if last_key is not None:
            assert key >= last_key
        last_key = key
        assert expected[key] == value