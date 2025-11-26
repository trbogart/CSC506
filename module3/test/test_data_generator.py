import random

from data_generator import generate_sorted, generate_unsorted, generate_reverse_sorted, generate_partially_sorted


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


def test_generate_unsorted():
    n = 10_000
    data = generate_unsorted(n)
    assert len(data) == n
    assert sum(data) == (n // 2) * (n + 1)  # sum of 1 to n

    unsorted_elements = get_unsorted_elements(data)
    assert unsorted_elements > n * 0.99


def test_generate_partially_sorted():
    n = 10_000
    data = generate_partially_sorted(n)
    assert len(data) == n
    assert sum(data) == (n // 2) * (n + 1)  # sum of 1 to n

    unsorted_elements = get_unsorted_elements(data)
    # expected 2 * n * 1%
    assert unsorted_elements > 100
    assert unsorted_elements < 300


def get_unsorted_elements(data: list[int]):
    count = 0
    for i, x in enumerate(data):
        if x != i + 1:
            count += 1
    return count
