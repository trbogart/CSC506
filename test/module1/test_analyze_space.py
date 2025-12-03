import math
import random

import pytest

from module1.complexity_analyzer import ComplexityAnalyzer


# Probabilistic test for ComplexityAnalyzer.analyze_space()

def test_analyze_space_1_nop():
    def op_new_size(_, old_size):
        return old_size

    AnalyzeSpaceTester(op_new_size).test('O(1)')


def test_analyze_space_1_add_in_init_op():
    def op_new_size(_, old_size):
        return old_size

    def init_op_new_size(i, old_size):
        return old_size + i  # ignore space added in init_op

    AnalyzeSpaceTester(op_new_size, init_op_new_size).test('O(1)')


def test_analyze_space_n():
    def op_new_size(_, old_size):
        return old_size + _noise()

    AnalyzeSpaceTester(op_new_size).test('O(n)')


@pytest.mark.skip('TODO fix log')
def test_analyze_space_log_n():
    def op_new_size(i, _):
        return math.log2(i + 1) * _noise()

    AnalyzeSpaceTester(op_new_size).test('O(log n)')

@pytest.mark.skip('TODO fix log')
def test_analyze_space_n_log_n():
    def new_size(i, old_size):
        return old_size + math.log2(i + 1) * _noise()

    AnalyzeSpaceTester(new_size).test('O(n log n)')


def test_analyze_space_n_2():
    def new_size(i, old_size):
        return old_size + i * _noise()

    AnalyzeSpaceTester(new_size).test('O(n^2)')


def _noise(noise=0.1):
    return 1.0 + random.uniform(-noise, noise)


class AnalyzeSpaceTester:
    def __init__(self, op_get_space, init_op_get_space=None, num_runs=1_000):
        self.size = 0
        self.op_get_space = op_get_space
        self.init_op_get_space = init_op_get_space
        self.analyzer = ComplexityAnalyzer(default_num_tests=1, default_num_runs=num_runs)

    def init_op(self, i):
        if self.init_op_get_space:
            self.size = self.init_op_get_space(i, self.size)

    def op(self, i):
        self.size = self.op_get_space(i, self.size)

    def get_estimated_space(self):
        return self.size

    def test(self, expected):
        actual = self.analyzer.analyze_space(self.op, self.get_estimated_space, init_op=self.init_op)
        assert actual == expected
