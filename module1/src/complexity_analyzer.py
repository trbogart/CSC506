import gc
import random
import time
import tracemalloc

import numpy as np
import matplotlib.pyplot as plt

"""
Estimates time or space complexity for an operation. 
Supports O(1), O(N), and O(N^2).
"""
# TODO add O(log(N)) and O(N*log(N))

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

    def analyze_time(self, op, title = None, init_test=None, init_op=None, post_op=None,
                     num_iterations=None, num_tests=None, threshold=None):
        return self.analyze(
            lambda _: time.perf_counter_ns(),
            op,
            title = title,
            y_axis = 'Time',
            init_test = init_test,
            init_op = init_op,
            post_op = post_op,
            num_iterations = num_iterations,
            num_tests = num_tests,
            threshold = threshold,
        )

    def analyze_space(self, op, title = None, init_test=None, init_op=None, post_op=None,
                      num_iterations=None, num_tests=None, threshold=None, full_gc=False):
        tracemalloc.start()

        def init_test_metric(_):
            # do a full garbage collection before each test unless already being done for each operation
            if not full_gc:
                gc.collect()

        result = self.analyze(
            lambda _: self._get_memory_usage(full_gc),
            op,
            title = title,
            y_axis = 'Space',
            init_test = init_test,
            init_op = init_op,
            post_op = post_op,
            init_test_metric = init_test_metric,
            num_iterations = num_iterations,
            num_tests = num_tests,
            threshold = threshold,
        )

        tracemalloc.stop()
        return result

    def analyze(self, metric, op, title = None, y_axis = None, init_test=None, init_op=None, post_op=None,
                init_test_metric=None, init_metric=None, post_metric=None,
                num_iterations=None, num_tests=None, threshold=None):
        """
        Estimates time complexity for the given operation.
        :param metric: metric to test (function with no arguments that returns a numeric value)
        :param op: operation to test (function with iteration number arguments)
        :param title: title to print with plot (ignored if plot not enabled)
        :param y_axis: name of y-axis (ignored if plot not enabled)
        :param init_test: initialize collection before each test (function with test number arguments)
        :param init_op: initialize operation (function with iteration number argument)
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

        def get_level(x_transformed, degree, level_name):
            coef = np.polyfit(x_transformed, metrics, degree)
            fit = np.poly1d(coef)
            y_pred = fit(x_transformed)
            return np.sqrt(np.mean((metrics - y_pred) ** 2)), x_transformed, y_pred, level_name

        # O(N^2)
        level_n_2 = get_level(x, 2, 'O(N^2)')

        # TODO fix log
        # # O(N * log(N))
        # x_n_log = np.log(x) * x
        # level_log_n_n = get_level(x_n_log, 1, 'O(N * log(N)))

        # O(N)
        level_n = get_level(x, 1, 'O(N)')

        # TODO fix log
        # # O(log(N))
        # x_log = np.log(x)
        # level_log_n = get_level(x_log, 1, 'O(log(N))')

        # O(1)
        level_1 = get_level(x, 0, 'O(1)')

        levels = [
            level_n_2,
            # level_log_n_n, # TODO fix log
            level_n,
            # level_log_n # TODO fix log
            level_1,
        ]

        def get_min_error(remaining_levels):
            return min(map(lambda level: level[0], remaining_levels))

        for i, (error, level_x, level_y, level_name) in enumerate(levels):
            if i == len(levels) - 1 or error * (1 + threshold) < get_min_error(levels[i + 1:]):
                if self.plot:
                    print(level_name)
                    fig, ax = plt.subplots()

                    ax.plot(x, metrics, label = 'Actual')
                    ax.plot(level_x, level_y, label = f'Estimated')

                    ax.set_xlabel('Size')
                    ax.set_ylabel(y_axis)
                    ax.legend()

                    subtitle = f'{title} {level_name}' if title else level_name
                    plt.suptitle(subtitle)
                    plt.tight_layout()
                    plt.show()
                return level_name

    @staticmethod
    def _get_memory_usage(full_gc):
        gc.collect(2 if full_gc else 1)
        current, _ = tracemalloc.get_traced_memory()
        return current

    def execute(self, collection, collection_type):
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
                # analyze time complexity for add
                def init_test(_):
                    collection.clear()

                def op(_):
                    collection.push(random.random())

                self.analyze_time(op, title=f'{collection_type} Add Time Complexity', init_test=init_test, num_iterations=2_000)
            elif cmd == 'tr':
                # analyze time complexity for remove
                num_iterations = 1_000
                def init_test(_):
                    collection.clear()
                    for i in range(num_iterations):
                        collection.push(random.random())

                def op(_):
                    collection.pop()

                self.analyze_time(op, title=f'{collection_type} Remove Time Complexity', init_test=init_test, num_iterations=num_iterations)
            elif cmd == 'ts':
                # analyze time complexity for search

                def init_test(_):
                    collection.clear()

                def init_op(i):
                    collection.push(i)

                def op(_):
                    collection.index(random.randint(1, len(collection)))

                self.analyze_time(op, title=f'{collection_type} Add Search Complexity', init_test=init_test, init_op=init_op, num_iterations=100)
            elif cmd == 'sa':
                # analyze space complexity for add
                num_iterations = 100

                def init_test(_):
                    collection.clear()

                def op(i):
                    collection.push(i)

                self.analyze_space(op, title=f'{collection_type} Add Space Complexity', init_test=init_test, num_iterations=num_iterations, full_gc=True)
            elif cmd == 'sr':
                # analyze space complexity for remove
                num_iterations = 100

                def init_test(_):
                    # start with full collection
                    collection.clear()
                    for _ in range(num_iterations):
                        collection.push(0)

                def op(_):
                    collection.pop()

                self.analyze_space(op, title=f'{collection_type} Remove Space Complexity', init_test=init_test, num_iterations=num_iterations, full_gc=True)
            elif cmd == 'ss':
                # analyze space complexity for search
                num_iterations = 100

                def init_test(_):
                    collection.clear()

                def init_op(i):
                    collection.push(i)

                def op(_):
                    collection.index(random.randint(1, len(collection)))

                self.analyze_space(op, title=f'{collection_type} Search Space Complexity', init_test=init_test, init_op=init_op, num_iterations=100, full_gc=True)
            else:
                print('Invalid command')
