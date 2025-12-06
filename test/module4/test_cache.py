import pytest

from module4.cache import Cache


def test_empty():
    cache = Cache[int, str](capacity=3)
    verify_cache(cache, {})
    assert 0 not in cache

    with pytest.raises(KeyError):
        _ = cache[0]


def test_add():
    cache = Cache[int, str](capacity=3)
    cache[1] = 'a'
    verify_cache(cache, {1: 'a'})
    cache[2] = 'b'
    verify_cache(cache, {2: 'b', 1: 'a'})


def test_add_to_capacity():
    cache = Cache[int, str](capacity=3)
    cache[1] = 'a'
    cache[2] = 'b'
    cache[3] = 'c'
    verify_cache(cache, {3: 'c', 2: 'b', 1: 'a'})

    # LRU entry drops off
    cache[4] = 'd'
    verify_cache(cache, {4: 'd', 3: 'c', 2: 'b'})
    cache[5] = 'e'
    verify_cache(cache, {5: 'e', 4: 'd', 3: 'c'})
    cache[6] = 'f'
    verify_cache(cache, {6: 'f', 5: 'e', 4: 'd'})

def test_update():
    cache = Cache[int, str](capacity=3)
    cache[1] = 'a'
    cache[2] = 'b'
    cache[3] = 'c'
    verify_cache(cache, {3: 'c', 2: 'b', 1: 'a'})
    cache[1] = 'd'
    verify_cache(cache, {1: 'd', 3: 'c', 2: 'b'})

    # add new item to verify that LRU was actually reset
    cache[4] = 'e'
    verify_cache(cache, {4: 'e', 1: 'd', 3: 'c'})


def test_update_to_same_value():
    cache = Cache[int, str](capacity=3)
    cache[1] = 'a'
    cache[2] = 'b'
    cache[3] = 'c'
    verify_cache(cache, {3: 'c', 2: 'b', 1: 'a'})
    cache[1] = 'a'
    verify_cache(cache, {1: 'a', 3: 'c', 2: 'b'})

    # add new item to verify that LRU was actually reset
    cache[4] = 'e'
    verify_cache(cache, {4: 'e', 1: 'a', 3: 'c'})


def test_get_only():
    cache = Cache[int, str](capacity=3)
    cache[1] = 'a'
    verify_cache(cache, {1: 'a'})

    assert cache[1] == 'a'
    verify_cache(cache, {1: 'a'})


def test_get_head():
    cache = Cache[int, str](capacity=3)
    cache[1] = 'a'
    cache[2] = 'b'
    cache[3] = 'c'
    verify_cache(cache, {3: 'c', 2: 'b', 1: 'a'})

    assert cache[3] == 'c'
    verify_cache(cache, {3: 'c', 2: 'b', 1: 'a'})

    # add new item to verify that LRU was actually reset
    cache[4] = 'd'
    verify_cache(cache, {4: 'd', 3: 'c', 2: 'b'})


def test_get_tail():
    cache = Cache[int, str](capacity=3)
    cache[1] = 'a'
    cache[2] = 'b'
    cache[3] = 'c'
    verify_cache(cache, {3: 'c', 2: 'b', 1: 'a'})

    assert cache[1] == 'a'
    verify_cache(cache, {1: 'a', 3: 'c', 2: 'b'})

    # add new item to verify that LRU was actually reset
    cache[4] = 'd'
    verify_cache(cache, {4: 'd', 1: 'a', 3: 'c'})


def test_get_middle():
    cache = Cache[int, str](capacity=3)
    cache[1] = 'a'
    cache[2] = 'b'
    cache[3] = 'c'
    verify_cache(cache, {3: 'c', 2: 'b', 1: 'a'})

    assert cache[2] == 'b'
    verify_cache(cache, {2: 'b', 3: 'c', 1: 'a'})

    # add new item to verify that LRU was actually reset
    cache[4] = 'd'
    verify_cache(cache, {4: 'd', 2: 'b', 3: 'c'})


def test_get_not_found():
    cache = Cache[int, str](capacity=3)
    cache[1] = 'a'
    with pytest.raises(KeyError):
        _ = cache[2]


def verify_cache(cache: Cache, expected: dict[int, str]):
    assert repr(cache) == repr(expected)
    assert len(cache) == len(expected)
    assert list(cache.keys()) == list(expected.keys())
    assert list(cache.values()) == list(expected.values())
    assert list(cache.items()) == list(expected.items())
