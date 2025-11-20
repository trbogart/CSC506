import math
from time import sleep

from complexity_analyzer import ComplexityAnalyzer


# Probabilistic test for ComplexityAnalyzer.analyze_time()

def test_analyze_time_1():
    def op(_):
        sleep(0)

    assert ComplexityAnalyzer().analyze_time(op, num_runs=100) == 'O(1)'


def test_analyze_time_n():
    def op(i):
        for _ in range(i):
            sleep(0)

    assert ComplexityAnalyzer().analyze_time(op, num_runs=100) == 'O(n)'


def test_analyze_time_log_n():
    def op(i):
        for _ in range(int(math.ceil(math.log2(i+1)))):
            sleep(0)

    assert ComplexityAnalyzer().analyze_time(op, num_runs=100) == 'O(log n)'


def test_analyze_time_n_log_n():
    def op(i):
        for _ in range(i * int(math.ceil(math.log2(i+1)))):
            sleep(0)

    assert ComplexityAnalyzer().analyze_time(op, num_runs=100) == 'O(n log n)'


def test_analyze_time_n_2():
    def op(i):
        for _ in range(i ** 2):
            sleep(0)

    assert ComplexityAnalyzer().analyze_time(op, num_runs=50) == 'O(n^2)'
