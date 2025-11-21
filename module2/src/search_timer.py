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
    default_base_size = 10
    default_num_sizes = 4  # check 4 sizes (10, 100, 1_000, and 10_000)
    default_num_tests = 5  # run 5 tests for each size
    log_slope_threshold = 1.1
    log_complexity = 'O(log n)'
    linear_complexity = 'O(n)'

    def __init__(self, description: str, search_op: Callable[[Iterable[int], int], int], sorted_data: bool):
        """
        Creates a search timer.
        :param description: description of the search algorithm (e.g. linear or binary)
        :param search_op: search operation
        :param sorted_data: true if the data must be sorted
        """
        self.description = description
        self.search_op = search_op
        self.sorted_data = sorted_data

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
        if not self.sorted_data:
            shuffle(a)
        total_time = 0

        # search for 10 evenly distributed values
        for i in range(num_samples):
            idx = i * size // num_samples
            value = idx if self.sorted_data else a[idx]
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
        for _ in range(num_sizes):
            elapsed_times.append(self.test_search(size, base_size, num_tests))
            size *= base_size
        complexity = self.get_complexity(elapsed_times)
        return SearchResults(base_size, num_sizes, elapsed_times, complexity)

    @staticmethod
    def get_complexity(elapsed_times: list[float]) -> str:
        """
        Estimates the time complexity based on the given elapsed times, which are for exponentially increasing sizes.
        :param elapsed_times: list of elapsed times
        :return: either `log_complexity` or `linear_complexity`
        """
        # I used Google AI search results and online tutorials for this portion (such as how to do polyfit and get
        # predicted values), but the logic is my own
        x = np.arange(0, len(elapsed_times))
        log_y = np.log(elapsed_times)
        coef = np.polyfit(x, log_y, 1)
        slope = coef[0]
        if slope < SearchTimer.log_slope_threshold:
            complexity = SearchTimer.log_complexity
        else:
            complexity = SearchTimer.linear_complexity

        return complexity


class LinearSearchTimer(SearchTimer):
    def __init__(self, sorted_data=False):
        super().__init__(description="Linear search", search_op=linear_search, sorted_data=sorted_data)


class BinarySearchTimer(SearchTimer):
    def __init__(self):
        super().__init__(description="Binary search", search_op=binary_search, sorted_data=True)
