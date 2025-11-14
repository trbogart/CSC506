import random
from bisect import bisect_left

import pytest
from flaky import flaky

from complexity_analyzer import ComplexityAnalyzer


# Probabilistic test for ComplexityAnalyzer.analyze_time()

def test_analyze_time_1():
    a = set()

    def init_test(_):
        a.clear()

    def init_op(i):
        a.add(i)

    def op(i):
        return i in a

    assert ComplexityAnalyzer().analyze_time(op, init_test=init_test, init_op=init_op, num_runs=5_000) == 'O(1)'

@pytest.mark.skip('TODO Fix log')
def test_analyze_time_log_n():
    a = []
    batch_size = 100

    def init_test(_):
        a.clear()

    def init_op(_):
        for _ in range(batch_size):
            a.append(len(a))

    def op(_):
        bisect_left(a, a[random.randint(0, len(a) - 1)])

    assert ComplexityAnalyzer().analyze_time(op, init_test=init_test, init_op=init_op,
                                             num_runs=100) == 'O(log(N))'


def test_analyze_time_n():
    a = []
    batch_size = 100

    def init_test(_):
        a.clear()

    def init_op(_):
        for _ in range(batch_size):
            a.append(random.random())

    def op(_):
        return a[random.randint(0, len(a) - 1)] in a

    assert ComplexityAnalyzer().analyze_time(op, init_test=init_test, init_op=init_op, num_runs=100) == 'O(N)'


@pytest.mark.skip('TODO Fix log')
@flaky(max_runs=2)  # somewhat flaky, but already slow enough that increasing runs is unappealing
def test_analyze_time_n_log_n():
    a = []
    batch_size = 1_000

    def init_test(_):
        a.clear()

    def init_op(_):
        for _ in range(batch_size):
            a.append(len(a))
        random.shuffle(a)

    def op(_):
        a.sort()

    assert ComplexityAnalyzer().analyze_time(op, init_test=init_test, init_op=init_op,
                                             num_runs=200) == 'O(N*log(N))'


def test_analyze_time_n_2():
    a = []
    batch_size = 5

    def init_test(_):
        a.clear()

    def init_op(_):
        for _ in range(batch_size):
            a.append(random.random())

    def op(_):
        for _ in a:
            for _ in a:
                pass

    assert ComplexityAnalyzer().analyze_time(op, init_test=init_test, init_op=init_op, num_runs=100) == 'O(N^2)'
