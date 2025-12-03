import random

from module3.data_generator import generate_sorted, generate_shuffled, generate_reverse_sorted, generate_partially_sorted


def setup_function():
    random.seed(1171)


def test_generate_sorted():
    n = 100
    data = generate_sorted(n)
    assert len(data) == n
    for i in range(n):
        assert data[i] == i + 1


def test_generate_reverse_sorted():
    n = 100
    data = generate_reverse_sorted(n)
    assert len(data) == n
    for i in range(n):
        assert data[n - i - 1] == i + 1


def test_generate_shuffled():
    n = 10_000
    data = generate_shuffled(n)
    assert len(data) == n
    assert sum(data) == (n // 2) * (n + 1)  # sum of 1 to n

    unsorted_elements = _get_unsorted_elements(data)
    assert unsorted_elements > n * 0.99


def test_generate_partially_sorted():
    n = 10_000
    data = generate_partially_sorted(n)
    assert len(data) == n

    unsorted_count = 0

    for i in range(n):
        assert data[i] >= i
        assert data[i] <= i + 2
        if i > 0 and data[i] < data[i - 1]:
            unsorted_count += 1

    assert unsorted_count > 0
    assert len(set(data)) < n  # have at least some duplicates


def _get_unsorted_elements(data: list[int]):
    count = 0
    for i, x in enumerate(data):
        if x != i + 1:
            count += 1
    return count
