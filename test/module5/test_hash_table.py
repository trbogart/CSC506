import math
import random

from module5.hash_table import HashTable


def test_empty():
    hashtable = HashTable()
    assert len(hashtable) == 0
    assert hashtable.num_deleted == 0

    assert hashtable.get(1) is None
    assert hashtable.delete(1) is None


def test_insert_new():
    hashtable = HashTable()

    assert hashtable.insert('a', 1) is None
    verify_hashtable(hashtable, {'a': 1})

    assert hashtable.insert('b', 2) is None
    verify_hashtable(hashtable, {'a': 1, 'b': 2})


def test_insert_update():
    hashtable = HashTable()

    assert hashtable.insert('a', 1) is None
    verify_hashtable(hashtable, {'a': 1})

    assert hashtable.insert('a', 2) == 1
    verify_hashtable(hashtable, {'a': 2})


def test_insert_collision():
    hashtable = HashTable(num_buckets=5)

    key1 = 1
    key2 = key1 + len(hashtable.buckets)  # same hashcode

    assert hashtable.insert(key1, 'a') is None
    assert hashtable.insert(key2, 'b') is None
    verify_hashtable(hashtable, {key1: 'a', key2: 'b'})


def test_get_missing():
    hashtable = HashTable(num_buckets=5)
    hashtable.insert(1, 1)
    for i in range(2, 10):
        assert i not in hashtable
        assert hashtable.get(i) is None


def test_resize():
    hashtable = HashTable()
    assert hashtable.max_added == HashTable.default_load_factor * HashTable.default_num_buckets
    bucket_sizes = {11, 23, 47, 97, 197}

    last_max_added = hashtable.max_added
    last_num_buckets = len(hashtable.buckets)

    expected = {}

    for key in range(100):
        value = key * key
        hashtable.insert(key, value)
        expected[key] = value
        verify_hashtable(hashtable, expected)

        if len(hashtable) >= last_max_added:
            # resized
            assert len(hashtable.buckets) > last_num_buckets
            assert len(hashtable.buckets) in bucket_sizes
            assert hashtable.max_added == hashtable.load_factor * len(hashtable.buckets)
            assert len(hashtable) <= hashtable.max_added
            last_max_added = hashtable.max_added
            last_num_buckets = len(hashtable.buckets)
        else:
            # not resized
            assert hashtable.max_added == last_max_added
            assert len(hashtable.buckets) == last_num_buckets

    assert hashtable.num_deleted == 0

def test_random():
    random.seed(137)
    hashtable = HashTable()
    expected = {}
    for i in range(1000):
        key = random.randint(0, 100_000)
        value = random.randint(0, 100_000)
        hashtable.insert(key, value)
        expected[key] = value
    verify_hashtable(hashtable, expected)


def test_delete_missing():
    hashtable = HashTable(num_buckets=5)
    assert hashtable.delete(5) is None
    assert hashtable.num_deleted == 0


def test_delete():
    hashtable = HashTable(num_buckets=5)

    key1 = 1

    assert hashtable.insert(key1, key1 ** 2) is None
    assert hashtable.delete(key1) == key1 ** 2
    verify_hashtable(hashtable, {})
    assert hashtable.num_deleted == 1


def test_delete_add():
    hashtable = HashTable(num_buckets=5)

    key1 = 1

    assert hashtable.insert(key1, key1 ** 2) is None
    assert hashtable.delete(key1) == key1 ** 2

    assert hashtable.insert(key1, key1) is None
    verify_hashtable(hashtable, {key1: key1})
    assert hashtable.num_deleted == 1

    assert hashtable.delete(key1) == key1
    verify_hashtable(hashtable, {})
    assert hashtable.num_deleted == 2


def test_delete_resize():
    hashtable = HashTable()
    assert hashtable.max_added == HashTable.default_load_factor * HashTable.default_num_buckets
    orig_max_added = hashtable.max_added
    hashtable.insert(1, 1)
    hashtable.delete(1)
    assert hashtable.num_deleted == 1

    expected = {}

    for key in range(2, int(math.ceil(hashtable.max_added))):
        hashtable.insert(key, key)
        expected[key] = key

        # not resized yet
        assert len(hashtable.buckets) == HashTable.default_num_buckets
        assert hashtable.num_deleted == 1
        assert hashtable.max_added == orig_max_added

    # adding 1 more should cause resize

    hashtable.insert(1, 1)
    expected[1] = 1
    assert len(hashtable.buckets) == 23
    assert hashtable.max_added == len(hashtable.buckets) * hashtable.load_factor
    assert hashtable.num_deleted == 0

    verify_hashtable(hashtable, expected)


def verify_hashtable(hashtable: HashTable, expected: dict):
    assert len(hashtable) == len(expected)

    for key, value in expected.items():
        assert key in hashtable
        assert hashtable.get(key) == value
