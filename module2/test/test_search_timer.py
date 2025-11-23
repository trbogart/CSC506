import math
import random

from search_timer import SearchTimer, LinearSearchTimer, BinarySearchTimer


def setup_function():
    random.seed(117)


expected_sizes = [10, 100, 1_000, 10_000]


def test_get_complexity_log():
    elapsed_times = _log_elapsed_times()
    complexity = SearchTimer.get_complexity(expected_sizes, elapsed_times)
    assert complexity == SearchTimer.log_complexity


def test_get_complexity_linear():
    elapsed_times = _linear_elapsed_times()
    complexity = SearchTimer.get_complexity(expected_sizes, elapsed_times)
    assert complexity == SearchTimer.linear_complexity


def test_search_timer_binary():
    timer = BinarySearchTimer()
    results = timer.test()
    assert results.complexity == SearchTimer.log_complexity
    assert results.base_size == SearchTimer.default_base_size
    assert results.num_elements == expected_sizes
    assert len(results.elapsed_times) == SearchTimer.default_num_sizes


def test_search_timer_linear():
    timer = LinearSearchTimer()
    results = timer.test()
    assert results.complexity == SearchTimer.linear_complexity
    assert results.base_size == SearchTimer.default_base_size
    assert results.num_elements == expected_sizes
    assert len(results.elapsed_times) == SearchTimer.default_num_sizes


def _log_elapsed_times():
    return [_get_random_elapsed_time(math.log2(expected_sizes[i])) for i in range(4)]


def _linear_elapsed_times():
    return [_get_random_elapsed_time(expected_sizes[i]) for i in range(4)]


def _get_random_elapsed_time(scale):
    return random.randint(1, 5) + scale * random.uniform(0.75, 1.25)
