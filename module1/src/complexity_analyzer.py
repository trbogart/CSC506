import gc
import random
import time
import tracemalloc

import numpy as np

"""
Estimates time or space complexity for an operation. 
Supports O(1), O(log(N)), O(N), O(N*log(N)), and O(N^2).
"""


class ComplexityAnalyzer:
    def __init__(self, plot = False, default_num_iterations = 10_000, default_num_tests = 5, default_threshold = 0.05):
        """
        Create complexity analyzer
        :param plot: true to plot values against expected
        :param default_num_iterations: default number of iterations per test (can be overridden in analyze methods)
        :param default_num_tests: default number of tests (can be overridden in analyze methods)
        :param default_threshold: default threshold (minimum proportion of error used to select higher level)
        """
        self.plot = plot
        self.default_num_iterations = default_num_iterations
        self.default_num_tests = default_num_tests
        self.default_threshold = default_threshold

    def analyze_time(self, op, init_test=None, init_op=None, post_op=None,
                     num_iterations=None, num_tests=None, threshold=None):
        return self.analyze(
            lambda _: time.perf_counter_ns(),
            op,
            init_test = init_test,
            init_op = init_op,
            post_op = post_op,
            num_iterations = num_iterations,
            num_tests = num_tests,
            threshold = threshold,
        )

    def analyze_space(self, op, init_test=None, init_op=None, post_op=None,
                      num_iterations=None, num_tests=None, threshold=None):
        tracemalloc.start()

        result = self.analyze(
            lambda _: self._get_memory_usage(),
            op,
            init_test = init_test,
            init_op = init_op,
            post_op = post_op,
            init_test_metric = lambda _: gc.collect(),
            num_iterations=num_iterations,
            num_tests=num_tests,
            threshold=threshold,
        )

        tracemalloc.stop()
        return result

    def analyze(self, metric, op, init_test=None, init_op=None, post_op=None,
                init_test_metric=None, init_metric=None, post_metric=None,
                num_iterations=None, num_tests=None, threshold=None):
        """
        Estimates time complexity for the given operation.
        :param metric: metric to test (function with no arguments that returns a numeric value)
        :param init_test: initialize collection before each test (function with test number arguments)
        :param init_op: initialize operation (function with iteration number argument)
        :param op: operation to test (function with iteration number arguments)
        :param post_op: cleanup after operation (function with iteration number argument)
        :param num_iterations number of iterations to test, or None to use the class default
        :param num_tests number of tests to run, or None to use the class default
        :param threshold: threshold (minimum proportion of error used to select higher level), or None to use the class default
        :param init_test_metric: initialize metric before each test (function with test number argument)
        :param init_metric: initialize metric (function with iteration number argument)
        :param post_metric: cleanup after gathering metric (function with no arguments)
        """
        metrics = [0] * num_iterations

        if num_tests is None:
            num_tests = self.default_num_tests
        if num_iterations is None:
            num_iterations = self.default_num_iterations
        if threshold is None:
            threshold = self.default_threshold

        for test in range(num_tests):
            if init_test:
                init_test(test + 1)
            if init_test_metric:
                init_test_metric(test + 1)
            for i in range(num_iterations):
                iter_num = i + 1
                if init_op:
                    init_op(iter_num)
                if init_metric:
                    init_metric(iter_num)
                start_metric = metric(iter_num)
                op(iter_num)
                end_metric = metric(iter_num)
                if post_op:
                    post_op(iter_num)
                if post_metric:
                    post_metric(iter_num)
                metrics[i] += end_metric - start_metric

        x = [i + 1 for i in range(num_iterations)]

        def get_error_and_coordinates(x_transformed, degree):
            coef = np.polyfit(x_transformed, metrics, degree)
            fit = np.poly1d(coef)
            y_pred = fit(x_transformed)
            return np.sqrt(np.mean((metrics - y_pred) ** 2))

        # O(N^2)
        error_quadratic = get_error_and_coordinates(x, 2)

        # O(N * log(N))
        x_n_log = np.log(x) * x
        error_n_log = get_error_and_coordinates(x_n_log, 1)

        # O(N)
        error_linear = get_error_and_coordinates(x, 1)

        # O(log(N))
        x_log = np.log(x)
        error_log = get_error_and_coordinates(x_log, 1)

        # O(1)
        error_constant = get_error_and_coordinates(x, 0)

        levels = [
            (error_quadratic, 'O(N^2)', threshold),
            (error_n_log, 'O(N*log(N))', threshold),
            (error_linear, 'O(N)', threshold),
            (error_log, 'O(log(N))', threshold),
            (error_constant, 'O(1)', None),
        ]

        def get_min_error(remaining_levels):
            return min(map(lambda level: level[0], remaining_levels))

        for i, (error, name, threshold) in enumerate(levels):
            if threshold is None or error * (1 + threshold) < get_min_error(levels[i + 1:]):
                if self.plot:
                    print(name)
                return name

    @staticmethod
    def _get_memory_usage():
        gc.collect(1)
        current, _ = tracemalloc.get_traced_memory()
        return current

    def execute(self, collection):
        while True:
            print('--------------------------------------------------------------')
            print('Enter command:')
            print('  ta) Analyze time complexity to add')
            print('  tr) Analyze time complexity to remove')
            print('  ts) Analyze time complexity to search for random element')
            print('  sa) Analyze space complexity to add')
            print('  sr) Analyze space complexity to remove')
            print('  ss) Analyze space complexity to search for random element')
            print('  q) Quit')
            cmd = input('> ')

            if cmd == 'q':
                collection.clear()
                return
            elif cmd == 'ta':
                def init_test(_):
                    collection.clear()

                def op(_):
                    collection.push(random.random())

                self.analyze_time(op, init_test=init_test, num_iterations=2000)
            elif cmd == 'tr':
                num_iterations = 1000
                def init_test(_):
                    collection.clear()
                    for i in range(num_iterations):
                        collection.push(random.random())

                def op(_):
                    collection.pop()

                self.analyze_time(op, init_test=init_test, num_iterations=num_iterations)
            elif cmd == 'ts':
                def init_test(_):
                    collection.clear()

                def init_op(_):
                    collection.push(len(collection))

                def op(_):
                    collection.index(random.randint(0, len(collection) - 1))

                self.analyze_time(op, init_test=init_test, init_op=init_op, num_iterations=100)
            else:
                print('Invalid command')
