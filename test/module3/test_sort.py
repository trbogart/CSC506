import random

from module3 import data_generator as dg, sort


def setup_function():
    random.seed(1171)


def test_bubble_sort_empty():
    _verify_sort(sort.bubble_sort, 0)


def test_bubble_sort_singleton():
    _verify_sort(sort.bubble_sort, 1)


def test_bubble_sort_shuffled():
    _verify_sort(sort.bubble_sort, 100)


def test_bubble_sort_already_sorted():
    _verify_sort(sort.bubble_sort, 100, already_sorted=True)


def test_bubble_sort_reverse_sorted():
    _verify_sort(sort.bubble_sort, 100, reverse_sorted=True)


def test_selection_sort_empty():
    _verify_sort(sort.selection_sort, 0)


def test_selection_sort_singleton():
    _verify_sort(sort.selection_sort, 1)


def test_selection_sort_shuffled():
    _verify_sort(sort.selection_sort, 100)


def test_selection_sort_already_sorted():
    _verify_sort(sort.selection_sort, 100, already_sorted=True)


def test_selection_sort_reverse_sorted():
    _verify_sort(sort.selection_sort, 100, reverse_sorted=True)


def test_insertion_sort_empty():
    _verify_sort(sort.insertion_sort, 0)


def test_insertion_sort_singleton():
    _verify_sort(sort.insertion_sort, 1)


def test_insertion_sort_shuffled():
    _verify_sort(sort.insertion_sort, 100)


def test_insertion_sort_already_sorted():
    _verify_sort(sort.insertion_sort, 100, already_sorted=True)


def test_insertion_sort_reverse_sorted():
    _verify_sort(sort.insertion_sort, 100, reverse_sorted=True)


def test_merge_sort_empty():
    _verify_sort(sort.merge_sort, 0)


def test_merge_sort_singleton():
    _verify_sort(sort.merge_sort, 1)


def test_merge_sort_shuffled():
    _verify_sort(sort.merge_sort, 100)


def test_merge_sort_already_sorted():
    _verify_sort(sort.merge_sort, 100, already_sorted=True)


def test_merge_sort_reverse_sorted():
    _verify_sort(sort.merge_sort, 100, reverse_sorted=True)


def test_pure_merge_sort_empty():
    _verify_sort(sort.merge_sort_pure, 0)


def test_pure_merge_sort_singleton():
    _verify_sort(sort.merge_sort_pure, 1)


def test_pure_merge_sort_shuffled():
    _verify_sort(sort.merge_sort_pure, 100)


def test_pure_merge_sort_already_sorted():
    _verify_sort(sort.merge_sort_pure, 100, already_sorted=True)


def test_pure_merge_sort_reverse_sorted():
    _verify_sort(sort.merge_sort_pure, 100, reverse_sorted=True)


def _verify_sort(sort_algorithm, n, already_sorted=False, reverse_sorted=False):
    if already_sorted or n <= 1:
        data = dg.generate_sorted(n)
    elif reverse_sorted:
        data = dg.generate_reverse_sorted(n)
    else:
        data = dg.generate_shuffled(n)

    sort_algorithm(data)

    assert len(data) == n
    for i in range(1, len(data)):
        assert data[i] >= data[i - 1]
