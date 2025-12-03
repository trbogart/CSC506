import random

import pytest

from module2.search_interface import SearchInterface
from module2.search_timer import LinearSearchTimer, SearchTimer, BinarySearchTimer


def setup_function():
    random.seed(117)


def test_constructor_default():
    si = SearchInterface()
    _validate_items_sorted(si, 0)


def test_constructor_unsorted():
    si = SearchInterface(is_sorted=False)
    _validate_items_unsorted(si, 0)


def test_constructor_sorted():
    si = SearchInterface(is_sorted=True)
    _validate_items_sorted(si, 0)


def test_constructor_empty():
    si = SearchInterface(size=0)
    _validate_items_sorted(si, 0)


def test_constructor_non_empty():
    si = SearchInterface(size=100)
    _validate_items_sorted(si, 100)


def test_constructor_non_empty_unsorted():
    si = SearchInterface(size=100, is_sorted=False)
    _validate_items_unsorted(si, 100)


def test_constructor_non_empty_sorted():
    si = SearchInterface(size=100, is_sorted=True)
    _validate_items_sorted(si, 100)


def test_set_size_unsorted():
    si = SearchInterface(is_sorted=False)
    si.set_size(10)
    _validate_items_unsorted(si, 10)
    si.set_size(20)
    _validate_items_unsorted(si, 20)
    si.set_size(5)
    _validate_items_unsorted(si, 5)
    si.set_size(0)
    _validate_items_unsorted(si, 0)


def test_set_size_sorted():
    si = SearchInterface(is_sorted=True)
    si.set_size(10)
    _validate_items_sorted(si, 10)
    si.set_size(20)
    _validate_items_sorted(si, 20)
    si.set_size(5)
    _validate_items_sorted(si, 5)
    si.set_size(0)
    _validate_items_sorted(si, 0)


def test_set_sorted_empty():
    si = SearchInterface(is_sorted=False)
    si.toggle_sorted()
    _validate_items_sorted(si, 0)


def test_set_sorted_non_empty():
    si = SearchInterface(100, is_sorted=False)
    si.toggle_sorted()
    _validate_items_sorted(si, 100)


def test_set_unsorted_empty():
    si = SearchInterface(is_sorted=True)
    si.toggle_sorted()
    _validate_items_unsorted(si, 0)


def test_set_unsorted_non_empty():
    si = SearchInterface(100, is_sorted=True)
    si.toggle_sorted()
    _validate_items_unsorted(si, 100)


def test_linear_search_unsorted_empty():
    si = SearchInterface(is_sorted=False)
    index, elapsed_time = si.linear_search(0)
    assert index == -1
    assert elapsed_time > 0


def test_linear_search_unsorted_not_found():
    si = SearchInterface(10, is_sorted=False)
    index, elapsed_time = si.linear_search(0)
    assert index == -1
    assert elapsed_time > 0


def test_linear_search_unsorted_found():
    si = SearchInterface(10, is_sorted=False)
    index, elapsed_time = si.linear_search(1)
    assert index >= 0
    assert elapsed_time > 0
    assert si.a[index] == 1


def test_linear_search_sorted_empty():
    si = SearchInterface(is_sorted=True)
    index, elapsed_time = si.linear_search(0)
    assert index == -1
    assert elapsed_time > 0


def test_linear_search_sorted_not_found():
    si = SearchInterface(10, is_sorted=True)
    index, elapsed_time = si.linear_search(0)
    assert index == -1
    assert elapsed_time > 0


def test_linear_search_sorted_found():
    si = SearchInterface(10, is_sorted=True)
    index, elapsed_time = si.linear_search(1)
    assert index == 0
    assert elapsed_time > 0


def test_binary_search_empty():
    si = SearchInterface(is_sorted=True)
    index, elapsed_time = si.binary_search(0)
    assert index == -1
    assert elapsed_time > 0


def test_binary_search_not_found():
    si = SearchInterface(10, is_sorted=True)
    index, elapsed_time = si.binary_search(0)
    assert index == -1
    assert elapsed_time > 0


def test_binary_search_found():
    si = SearchInterface(10, is_sorted=True)
    index, elapsed_time = si.binary_search(1)
    assert index == 0
    assert elapsed_time > 0
    assert si.a[index] == 1


def test_run_linear_performance_tests():
    si = SearchInterface(10)
    original_list = si.a
    results = si.run_performance_tests(LinearSearchTimer())
    assert results.complexity == SearchTimer.linear_complexity

    # original list unchanged
    assert si.a == original_list


def test_run_binary_performance_tests():
    si = SearchInterface(10, is_sorted=True)
    original_list = si.a
    results = si.run_performance_tests(BinarySearchTimer())
    assert results.complexity == SearchTimer.log_complexity

    # original list unchanged
    assert si.a == original_list


def _validate_items_unsorted(si: SearchInterface, size: int) -> None:
    assert si.is_sorted == False
    assert len(si.a) == size
    expected_values = {i + 1 for i in range(size)}
    actual_values = set(si.a)
    assert actual_values == expected_values

    if size > 0:
        for i in range(1, size):
            if si.a[i - 1] > si.a[i]:
                # found at least 1 unsorted value
                break
        else:
            pytest.fail('List should not be sorted')


def _validate_items_sorted(si: SearchInterface, size: int) -> None:
    assert si.is_sorted == True
    assert len(si.a) == size
    for i in range(size):
        assert si.a[i] == i + 1
