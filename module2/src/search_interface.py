import random
import sys
from time import perf_counter
from typing import Callable, Iterable

import search
from search_timer import SearchTimer, LinearSearchTimer, BinarySearchTimer, SearchResults


class SearchInterface:
    max_size = 10_000_000

    def __init__(self, size=0, is_sorted=True):
        self.a = []
        self.is_sorted = is_sorted
        self.set_size(size)

    @staticmethod
    def get_int_input(min_value=0, max_value=max_size, prompt=None):
        if prompt is None:
            prompt = f'Enter a number between {min_value:,} and {max_value:,}: '
        while True:
            try:
                cmd = int(input(prompt).replace(',',''))
                if min_value <= cmd <= max_value:
                    return cmd
            except ValueError:
                pass
            print('Invalid input. Try again.')

    def print_menu(self):
        binary_prefix = '' if self.is_sorted else 'DISABLED (UNSORTED) - '
        print('------------------------------------------------------------')
        print(f'List has {len(self.a):,} {'sorted' if self.is_sorted else 'unsorted'} elements')
        print('0) Exit')
        print('1) Set size')
        print('2) Toggle sorted')
        print('3) List elements')
        print('4) Linear search for value')
        print(f'5) {binary_prefix}Binary search for value')
        print('6) Run performance tests for linear search (will not effect current list)')
        print(f'7) {binary_prefix}Run performance tests for binary search (will not effect current list)')
        cmd = self.get_int_input(0, 7)
        if cmd == 0:
            # exit
            sys.exit(0)
        elif cmd == 1:
            # set size
            new_size = self.get_int_input()
            self.set_size(new_size)
        elif cmd == 2:
            # toggle sorted
            self.toggle_sorted()
        elif cmd == 3:
            # list elements
            size = len(self.a)
            if size == 0:
                print('List is empty')
            else:
                max_items = 50
                num_shown_items = 20 if size > max_items else size
                for i in range(num_shown_items):
                    print(f'[#{i + 1}]: {self.a[i]}')
                if size > num_shown_items:
                    print(f'... {size - num_shown_items - 1} items excluded')
                    print(f'[#{size}]: {self.a[size - 1]}')
        elif cmd == 4:
            # linear search
            value = self.get_search_value()
            self.linear_search(value)
        elif cmd == 5:
            # binary search (disabled if not sorted)
            if self.is_sorted:
                value = self.get_search_value()
                self.binary_search(value)
            else:
                print('Must be sorted')
        elif cmd == 6:
            # linear performance test
            self.run_performance_tests(LinearSearchTimer())
        elif cmd == 7:
            # binary performance test (disabled if not sorted)
            if self.is_sorted:
                self.run_performance_tests(BinarySearchTimer())
            else:
                print('Must be sorted')

    def get_search_value(self):
        if len(self.a) > 0:
            suffix = f'(values between 1 and {len(self.a):,} will be found)'
        else:
            suffix = '(no values will be found)'
        return self.get_int_input(prompt=f'Enter a value {suffix}: ')

    def set_size(self, new_size: int) -> None:
        if new_size != len(self.a):
            self.a = self.new_sorted_list(new_size)
            if not self.is_sorted:
                random.shuffle(self.a)

    def toggle_sorted(self) -> None:
        self.is_sorted = not self.is_sorted
        if self.is_sorted:
            self.a = self.new_sorted_list(len(self.a))
        else:
            random.shuffle(self.a)

    def linear_search(self, value: int) -> (int, float):
        return self.do_search(value, "Linear search", search.linear_search)

    def binary_search(self, value: int) -> (int, float):
        self._validate_sorted()
        return self.do_search(value, "Binary search", search.binary_search)

    def do_search(self, value: int, description: str, search_op: Callable[[Iterable[int], int], int]) -> (int, float):
        start_time = perf_counter()
        try:
            index = search_op(self.a, value)
        except ValueError:
            index = -1
        elapsed_time = perf_counter() - start_time
        print(
            f'{description} took {elapsed_time * 1000:.4f} ms over {len(self.a):,} items: {index if index > 0 else "not found"}')
        return index, elapsed_time

    def _validate_sorted(self):
        if not self.is_sorted:
            raise ValueError('List must be sorted')

    def run_performance_tests(self, search_timer: SearchTimer) -> SearchResults:
        if search_timer.requires_sorted:
            self._validate_sorted()
        results = search_timer.test()
        print(f'{search_timer.description} ran in {results.complexity} time')
        for i in range(results.num_sizes):
            print(
                f'  Average time for {results.num_elements[i]:,} elements: {results.elapsed_times[i] * 1000:.4f} ms')

        return results

    @staticmethod
    def new_sorted_list(new_size: int):
        return [i + 1 for i in range(new_size)]


if __name__ == '__main__':
    s = SearchInterface()
    while True:
        s.print_menu()
