import array as arr
import itertools
import math
import sys

from complexity_analyzer import ComplexityAnalyzer


# Probabilistic test for ComplexityAnalyzer.analyze_space()

def test_analyze_space_1_nop():
    def op(_):
        pass

    def get_estimated_space():
        return 0

    assert (ComplexityAnalyzer(default_num_tests=1)
            .analyze_space(op, get_estimated_space, num_runs=10) == 'O(1)')


def test_analyze_space_1_add_in_init_op():
    a = ArrayWrapper()

    def init_test(_):
        a.clear()

    def init_op(_):
        a.add_elements(1)

    def op(_):
        pass

    def get_estimated_space():
        return a.get_estimated_space()

    assert (ComplexityAnalyzer(default_num_tests=1)
            .analyze_space(op, get_estimated_space, init_op=init_op, init_test=init_test, num_runs=10) == 'O(1)')


def test_analyze_space_n():
    a = ArrayWrapper()

    def init_test(_):
        a.clear()

    def op(_):
        a.add_elements(1)

    def get_estimated_space():
        return a.get_estimated_space()

    assert (ComplexityAnalyzer(default_num_tests=1)
            .analyze_space(op, get_estimated_space, init_test=init_test, num_runs=100) == 'O(n)')


def test_analyze_space_log_n():
    a = ArrayWrapper()

    def init_test(_):
        a.clear()

    def op(n):
        a.set_size(int(math.ceil(math.log2(n + 1))))

    def get_estimated_space():
        return a.get_estimated_space()

    assert (ComplexityAnalyzer(default_num_tests=1)
            .analyze_space(op, get_estimated_space, init_test=init_test, num_runs=5_000) == 'O(log n)')


def test_analyze_space_n_log_n():
    a = ArrayWrapper()

    def init_test(_):
        a.clear()

    def op(n):
        a.add_elements(int(math.ceil(math.log2(n + 1))))

    def get_estimated_space():
        return a.get_estimated_space()

    assert (ComplexityAnalyzer(default_num_tests=1)
            .analyze_space(op, get_estimated_space, init_test=init_test, num_runs=1_000) == 'O(n log n)')


def test_analyze_space_n_2():
    a = ArrayWrapper()

    def init_test(_):
        a.clear()

    def op(n):
        a.add_elements(n)

    def get_estimated_space():
        return a.get_estimated_space()

    assert (ComplexityAnalyzer(default_num_tests=1)
            .analyze_space(op, get_estimated_space, init_test=init_test, num_runs=10) == 'O(n^2)')


# wrapper to test memory usage more precisely
class ArrayWrapper:
    def __init__(self):
        self.a = self._allocate(0)

    def set_size(self, size):
        if size != len(self.a):
            self.a = self._allocate(size)

    def add_elements(self, delta):
        if delta != 0:
            self.a = self._allocate(len(self.a) + delta)

    def clear(self):
        self.a = self._allocate(0)

    @staticmethod
    def _allocate(size):
        return arr.array('i', itertools.repeat(0, size))

    def get_estimated_space(self):
        """Helper method to get the estimated space consumed by this list"""
        return sys.getsizeof(self) + sys.getsizeof(self.a)
