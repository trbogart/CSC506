from bisect import bisect_left

import pytest

from complexity_analyzer import ComplexityAnalyzer
import random

def test_analyze_1():
    a = set()

    def init_test(_):
        a.clear()

    def init_op(i):
        a.add(i)

    def op(i):
        return i in a

    assert ComplexityAnalyzer().analyze_time(init_test, init_op, op, num_iterations = 2_000) == 'O(1)'

@pytest.mark.skip(reason = 'TODO fix log')
def test_analyze_log_n():
    a = []
    batch_size = 20

    def init_test(_):
        a.clear()

    def init_op(batch):
        for i in range(batch_size):
            a.append(batch * batch_size + i)

    def op(_):
        bisect_left(a, a[0])

    assert ComplexityAnalyzer().analyze_time(init_test, init_op, op, num_iterations = 2_000) == 'O(log(N))'

def test_analyze_n():
    a = []
    batch_size = 20

    def init_test(_):
        a.clear()

    def init_op(_):
        for _ in range(batch_size):
            a.append(random.random())

    def op(_):
        return a[-1] in a

    assert ComplexityAnalyzer().analyze_time(init_test, init_op, op, num_iterations = 2_000) == 'O(N)'

@pytest.mark.skip(reason = 'TODO fix log')
def test_analyze_n_log_n():
    a = []
    batch_size = 20

    def init_test(_):
        a.clear()

    def init_op(_):
        for _ in range(batch_size):
            a.append(random.random())
        random.shuffle(a)

    def op(_):
        a.sort()

    assert ComplexityAnalyzer().analyze_time(init_test, init_op, op, num_iterations = 1_000) == 'O(N*log(N))'

def test_analyze_n_2():
    a = []
    batch_size = 20

    def init_test(_):
        a.clear()

    def init_op(_):
        for _ in range(batch_size):
            a.append(random.random())

    def op(_):
        for _ in a:
            for _ in a:
                pass

    assert ComplexityAnalyzer().analyze_time(init_test, init_op, op, num_iterations = 100) == 'O(N^2)'
