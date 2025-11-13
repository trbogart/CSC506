from bisect import bisect_left

from flaky import flaky

from complexity_analyzer import ComplexityAnalyzer
import random

# Probabilistic test for ComplexityAnalyzer

def test_analyze_1():
    a = set()

    def init_test(_):
        a.clear()

    def init_op(i):
        a.add(i)

    def op(i):
        return i in a

    assert ComplexityAnalyzer().analyze_time(init_test, init_op, op, num_iterations = 5_000) == 'O(1)'

def test_analyze_log_n():
    a = []
    batch_size = 100

    def init_test(_):
        a.clear()

    def init_op(_):
        for _ in range(batch_size):
            a.append(len(a))

    def op(_):
        bisect_left(a, a[random.randint(0, len(a) - 1)])

    assert ComplexityAnalyzer().analyze_time(init_test, init_op, op, num_iterations = 10_000) == 'O(log(N))'

def test_analyze_n():
    a = []
    batch_size = 100

    def init_test(_):
        a.clear()

    def init_op(_):
        for _ in range(batch_size):
            a.append(random.random())

    def op(_):
        return a[random.randint(0, len(a)-1)] in a

    assert ComplexityAnalyzer().analyze_time(init_test, init_op, op, num_iterations = 1_000) == 'O(N)'

@flaky(max_runs = 2) # somewhat flaky, but already slow enough that increasing iterations is unappealing
def test_analyze_n_log_n():
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

    assert ComplexityAnalyzer().analyze_time(init_test, init_op, op, num_iterations = 200) == 'O(N*log(N))'

def test_analyze_n_2():
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

    assert ComplexityAnalyzer().analyze_time(init_test, init_op, op, num_iterations = 100) == 'O(N^2)'
