import random

import pytest

from module2.search import binary_search, linear_search


def setup_function():
    random.seed(117)


def test_binary_search_empty():
    with pytest.raises(ValueError):
        binary_search([], 1)


def test_binary_search_not_found():
    with pytest.raises(ValueError):
        binary_search([1, 2, 3], 0)


def test_binary_search_10():
    _test_binary_search(10)


def test_binary_search_100():
    _test_binary_search(100)


def test_binary_search_1_000():
    _test_binary_search(1_000)


def test_binary_search_10_000():
    _test_binary_search(10_000)


def test_linear_search_empty():
    with pytest.raises(ValueError):
        linear_search([], 1)


def test_linear_search_not_found():
    with pytest.raises(ValueError):
        linear_search([1, 2, 3], 0)


def test_linear_search_10():
    _test_linear_search(10)


def test_linear_search_100():
    _test_linear_search(100)


def test_linear_search_1_000():
    _test_linear_search(1_000)


def test_linear_search_10_000():
    _test_linear_search(10_000)


def _test_linear_search(count):
    a = [i for i in range(count)]
    random.shuffle(a)
    _test_search(a, linear_search)


def _test_binary_search(count):
    a = [i for i in range(count)]
    _test_search(a, binary_search)


def _test_search(a, search_op):
    skip = 1 if len(a) < 1_000 else len(a) // 10
    for i in range(0, len(a), skip):
        assert search_op(a, a[i]) == i
    with pytest.raises(ValueError):
        search_op(a, -1)
