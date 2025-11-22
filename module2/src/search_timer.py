from random import shuffle
from time import perf_counter
from typing import Callable, Iterable

import numpy as np

from search import binary_search, linear_search


class SearchResults:
    def __init__(self, base_size: int, num_sizes: int, elapsed_times: list[float], complexity: str):
        """
        Search results.

        :param base_size: smallest size that was tested
        :param num_sizes: number of size steps tested (multiply previous size by base_size)
        :param elapsed_times: list of elapsed times
        :param complexity: estimated complexity for search ('O(n)' or 'O(log n)')
        """
        self.base_size = base_size
        self.num_sizes = num_sizes
        self.num_elements = [base_size ** batch for batch in range(1, num_sizes + 1)]
        self.elapsed_times = elapsed_times
        self.complexity = complexity


class SearchTimer:
    """
    Runs search performance tests.
    """
    default_base_size = 10
    default_num_sizes = 4  # check 4 sizes (10, 100, 1_000, and 10_000)
    default_num_tests = 5  # run 5 tests for each size
    log_complexity = 'O(log n)'
    linear_complexity = 'O(n)'

    def __init__(self, description: str, search_op: Callable[[Iterable[int], int], int], requires_sorted: bool):
        """
        Creates a search timer.
        :param description: description of the search algorithm (e.g. linear or binary)
        :param search_op: search operation
        :param requires_sorted: true if the data must be sorted
        """
        self.description = description
        self.search_op = search_op
        self.requires_sorted = requires_sorted

    def test_search(self, size: int, num_samples: int, num_tests: int) -> float:
        """
        Creates an array of the given size and performs the requested search over an evenly distributed sample of values.
        The array will be sorted

        :param size: size of the array to search
        :param num_samples: number of samples to tests
        :param num_tests: number of times to repeat each search
        :return: average search time
        """
        a = [i for i in range(size)]
        if not self.requires_sorted:
            shuffle(a)
        total_time = 0

        # search for 10 evenly distributed values
        for i in range(num_samples):
            idx = i * size // num_samples
            value = idx if self.requires_sorted else a[idx]
            for _ in range(num_tests):
                start_time = perf_counter()
                self.search_op(a, value)
                total_time += perf_counter() - start_time
        elapsed_time = total_time / (num_samples * num_tests)
        return elapsed_time

    def test(self, num_tests=default_num_tests, base_size=default_base_size,
             num_sizes=default_num_sizes) -> SearchResults:
        """
        Performs a search over multiple exponentially increasing sizes.
        :param base_size: base size for search (defaults to 10)
        :param num_sizes: number of exponential increasing sizes to test (defaults to 4)
        """
        size = base_size

        # do an unmeasured initial priming run
        self.test_search(size, base_size, num_tests=1)

        elapsed_times = []
        sizes = []
        for _ in range(num_sizes):
            sizes.append(size)
            elapsed_times.append(self.test_search(size, base_size, num_tests))
            size *= base_size
        complexity = self.get_complexity(sizes, elapsed_times)
        return SearchResults(base_size, num_sizes, elapsed_times, complexity)

    @staticmethod
    def get_complexity(x: list[int], y: list[float]) -> str:
        """
        Estimates the time complexity based on the given elapsed times, which are for exponentially increasing sizes.
        :param x: x values
        :param y: y values
        :return: either `log_complexity` or `linear_complexity`
        """
        # I used Google AI search results and online tutorials for this portion (such as how to do polyfit and get
        # predicted values), but the logic is my own

        # log fit
        log_x = np.log(x)
        log_y = np.log(y)
        log_coef = np.polyfit(log_x, log_y, 1)
        log_y_pred = np.exp(np.poly1d(log_coef)(log_x))
        log_error = np.sqrt(np.sum((log_y_pred - y) ** 2))

        # linear fit
        linear_coef = np.polyfit(x, y, 1)
        linear_y_pred = np.poly1d(linear_coef)(x)
        linear_error = np.sqrt(np.sum((linear_y_pred - y) ** 2))

        if log_error < linear_error:
            complexity = SearchTimer.log_complexity
        else:
            complexity = SearchTimer.linear_complexity

        return complexity


class LinearSearchTimer(SearchTimer):
    def __init__(self):
        super().__init__(description="Linear search", search_op=linear_search, requires_sorted=False)


class BinarySearchTimer(SearchTimer):
    def __init__(self):
        super().__init__(description="Binary search", search_op=binary_search, requires_sorted=True)
