import random

from module8.set import Set


def test_empty():
    s = Set()
    _verify(s)
    assert 1 not in s


def test_insert():
    s = Set()
    assert s.add(1)
    _verify(s, 1)

    # insert duplicate
    assert not s.add(1)
    _verify(s, 1)

    assert s.add(2)
    _verify(s, 1, 2)


def test_clear():
    s = Set()
    s.add(1)
    s.add(2)
    s.add(3)
    s.clear()
    _verify(s)
    assert len(s.buckets) == s.start_num_buckets


def test_insert_resize():
    s = Set()
    expected = set()
    for i in range(200):
        expected.add(i)
        s.add(i)
        _verify_set(s, expected)


def test_remove():
    s = Set()
    s.add(1)
    s.add(2)
    s.add(3)
    _verify(s, 1, 2, 3)
    assert s.remove(2)
    _verify(s, 1, 3)
    assert not s.remove(2)
    _verify(s, 1, 3)
    assert s.remove(1)
    _verify(s, 3)
    assert s.remove(3)
    _verify(s)
    assert not s.remove(3)


def test_insert_chain():
    # insert multiple entries into same bucket
    s = Set()
    value1 = 1
    value2 = value1 + len(s.buckets)
    value3 = value2 + len(s.buckets)

    idx1 = s._get_index(value1)
    idx2 = s._get_index(value2)
    idx3 = s._get_index(value3)

    assert idx1 == idx2 == idx3

    s.add(value1)
    s.add(value2)
    s.add(value3)
    _verify(s, value1, value2, value3)

    bucket = s.buckets[idx1]
    assert bucket is not None
    assert bucket.value == value3
    assert bucket.next_bucket is not None
    assert bucket.next_bucket.value == value2
    assert bucket.next_bucket.next_bucket is not None
    assert bucket.next_bucket.next_bucket.value == value1
    assert bucket.next_bucket.next_bucket.next_bucket is None


def test_remove_chain1():
    s = Set()
    value1 = 1
    value2 = value1 + len(s.buckets)
    value3 = value2 + len(s.buckets)

    s.add(value3)
    s.add(value2)
    s.add(value1)

    s.remove(value1)
    _verify(s, value2, value3)


def test_remove_chain2():
    s = Set()
    value1 = 1
    value2 = value1 + len(s.buckets)
    value3 = value2 + len(s.buckets)

    s.add(value3)
    s.add(value2)
    s.add(value1)

    s.remove(value2)
    _verify(s, value1, value3)


def test_remove_chain3():
    s = Set()
    value1 = 1
    value2 = value1 + len(s.buckets)
    value3 = value2 + len(s.buckets)

    s.add(value3)
    s.add(value2)
    s.add(value1)

    s.remove(value3)
    _verify(s, value1, value2)


def test_resize():
    s = Set()
    for i in range(8):
        s.add(i)
        assert len(s.buckets) == 11
    for i in range(8, 17):
        assert s.add(i)
        assert len(s.buckets) == 23
    for i in range(17, 20):
        assert s.add(i)
        assert len(s.buckets) == 47

    for i in range(0, 3):
        assert s.remove(i)
        assert len(s.buckets) == 47
    for i in range(3, 12):
        assert s.remove(i)
        assert len(s.buckets) == 23
    for i in range(12, 20):
        assert s.remove(i)
        assert len(s.buckets) == 11


def test_random():
    random.seed(1732)
    bucket_sizes = {11, 23, 47, 97, 197}
    data = [i + 1 for i in range(100)]

    # add data in multiple orders
    for _ in range(100):
        random.shuffle(data)
        expected = set()

        s = Set()
        for item in data:
            s.add(item)
            expected.add(item)
            _verify_set(s, expected)
            assert len(s.buckets) in bucket_sizes
            assert len(s) < len(s.buckets) * s.load_factor

        random.shuffle(data)
        for item in data:
            s.remove(item)
            expected.remove(item)
            _verify_set(s, expected)
            assert len(s.buckets) in bucket_sizes

        assert len(s) == 0
        assert len(s.buckets) == 11


def test_union():
    s1 = set()
    s2 = set()

    s1.add(1)
    s1.add(2)
    s1.add(3)

    s2.add(2)
    s2.add(3)
    s2.add(4)

    _verify(s1.union(s2), 1, 2, 3, 4)
    _verify(s2.union(s1), 1, 2, 3, 4)


def test_intersection():
    s1 = set()
    s2 = set()

    s1.add(1)
    s1.add(2)
    s1.add(3)

    s2.add(2)
    s2.add(3)
    s2.add(4)

    _verify(s1.intersection(s2), 2, 3)
    _verify(s2.intersection(s1), 2, 3)


def test_difference():
    s1 = set()
    s2 = set()

    s1.add(1)
    s1.add(2)
    s1.add(3)

    s2.add(2)
    s2.add(3)
    s2.add(4)

    _verify(s1.difference(s2), 1)
    _verify(s2.difference(s1), 4)


def test_symmetric_difference():
    s1 = set()
    s2 = set()

    s1.add(1)
    s1.add(2)
    s1.add(3)

    s2.add(2)
    s2.add(3)
    s2.add(4)

    _verify(s1.symmetric_difference(s2), 1, 4)
    _verify(s2.symmetric_difference(s1), 1, 4)


def _verify_set(s, expected_set):
    # verify __length__
    assert len(s) == len(expected_set)

    # verify __contains__
    for item in expected_set:
        assert item in s

    # verify __iter__
    for item in iter(s):
        assert item in expected_set


def _verify(s, *expected):
    _verify_set(s, set(expected))
