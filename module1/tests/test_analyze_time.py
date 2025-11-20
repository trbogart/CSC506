import math
import random

from complexity_analyzer import ComplexityAnalyzer


# Probabilistic test for ComplexityAnalyzer.analyze_time()

def test_analyze_time_1():
    def op_elapsed_time(_):
        return 1

    AnalyzeTimeTester(op_elapsed_time).test('O(1)')


def test_analyze_time_n():
    def op_elapsed_time(i):
        return i

    AnalyzeTimeTester(op_elapsed_time).test('O(n)')


def test_analyze_time_log_n():
    def op_elapsed_time(i):
        return math.log2(i + 1)

    AnalyzeTimeTester(op_elapsed_time).test('O(log n)')


def test_analyze_time_n_log_n():
    def op_elapsed_time(i):
        return i * math.log2(i + 1)

    AnalyzeTimeTester(op_elapsed_time).test('O(n log n)')


def test_analyze_time_n_2():
    def op_elapsed_time(i):
        return i ** 2

    AnalyzeTimeTester(op_elapsed_time).test('O(n^2)')


class AnalyzeTimeTester:
    def __init__(self, op_elapsed_time, num_runs=1_000, noise=0.1):
        self.analyzer = ComplexityAnalyzer(default_num_tests=1, default_num_runs=num_runs)
        self.current_time = 1_000_000
        self.noise = noise
        self.op_elapsed_time = op_elapsed_time

    def get_current_time(self):
        return self.current_time

    def op(self, i):
        self.current_time += self.op_elapsed_time(i) * random.uniform(1.0 - self.noise, 1.0 + self.noise)

    def test(self, expected):
        actual = self.analyzer.analyze_time(self.op, timer=self.get_current_time)
        assert actual == expected
