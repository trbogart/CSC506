import array as arr
import itertools
import math
from complexity_analyzer import ComplexityAnalyzer

# Probabilistic test for ComplexityAnalyzer.analyze_space()

def test_analyze_space_1():
    def op(_):
        pass

    assert ComplexityAnalyzer().analyze_space(op, num_iterations = 1_000) == 'O(1)'

def test_analyze_space_log_n():
    a = ArrayWrapper()
    batch_size = 1_000

    def init_test(_):
        a.clear()

    def op(i):
        a.add_elements(batch_size * int(math.ceil(math.log2(i + 1))))

    assert ComplexityAnalyzer().analyze_space(op, init_test = init_test, num_iterations = 2_000) == 'O(log(N))'

def test_analyze_space_n():
    a = ArrayWrapper()
    batch_size = 100

    def init_test(_):
        a.clear()

    def op(_):
        a.add_elements(batch_size)

    assert ComplexityAnalyzer().analyze_space(op, init_test = init_test, num_iterations = 100) == 'O(1)'


def test_analyze_space_n_log_n():
    a = ArrayWrapper()
    batch_size = 1_000

    def init_test(_):
        a.clear()

    def op(i):
        a.add_elements(batch_size * i * int(math.ceil(math.log2(i+1))))

    assert ComplexityAnalyzer().analyze_space(op, init_test = init_test, num_iterations = 1_000) == 'O(N*log(N))'

def test_analyze_space_n_2():
    a = ArrayWrapper()
    batch_size = 100

    def init_test(_):
        a.clear()

    def op(i):
        a.add_elements(batch_size * i)

    assert ComplexityAnalyzer().analyze_space(op, init_test = init_test, num_iterations = 1_000) == 'O(N^2)'

# wrapper to test memory usage more precisely
class ArrayWrapper:
    def __init__(self):
        self.a = self._allocate(0)

    def add_elements(self, delta):
        if delta != 0:
            self.a = self._allocate(len(self.a) + delta)

    def clear(self):
        self.a = self._allocate(0)

    @staticmethod
    def _allocate(size):
        return arr.array('i', itertools.repeat(0, size))
