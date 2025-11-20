import math

from complexity_analyzer import ComplexityAnalyzer


# Probabilistic test for ComplexityAnalyzer.analyze_space()

def test_analyze_space_1_nop():
    def new_size(_, old_size):
        return old_size
    SpaceTester(new_size).test_analyze_space('O(1)')


def test_analyze_space_1_add_in_init_op():
    def new_size(_, old_size):
        return old_size
    def init_op_new_size(i, old_size):
        return old_size + i # ignore space added in init_op
    SpaceTester(new_size, init_op_new_size).test_analyze_space('O(1)')


def test_analyze_space_n():
    def new_size(_, old_size):
        return old_size + 1
    SpaceTester(new_size).test_analyze_space('O(n)')


def test_analyze_space_log_n():
    def new_size(i, _):
        return math.log2(i+1)
    SpaceTester(new_size).test_analyze_space('O(log n)')


def test_analyze_space_n_log_n():
    def new_size(i, old_size):
        return old_size + math.log2(i+1)
    SpaceTester(new_size).test_analyze_space('O(n log n)')


def test_analyze_space_n_2():
    def new_size(i, old_size):
        return old_size + i
    SpaceTester(new_size).test_analyze_space('O(n^2)')


class SpaceTester:
    def __init__(self, op_get_space, init_op_get_space = None):
        self.size = 0
        self.op_get_space = op_get_space
        self.init_op_get_space = init_op_get_space

    def init_op(self, i):
        if self.init_op_get_space:
            self.size = self.init_op_get_space(i, self.size)

    def op(self, i):
        self.size = self.op_get_space(i, self.size)

    def get_estimated_space(self):
        return self.size

    def test_analyze_space(self, expected, num_runs = 20):
        actual = (ComplexityAnalyzer(default_num_tests=1)
                  .analyze_space(self.op, self.get_estimated_space, init_op = self.init_op, num_runs=num_runs))
        assert actual == expected


