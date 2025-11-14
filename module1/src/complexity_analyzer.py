import random
import time

import matplotlib.pyplot as plt
import numpy as np

"""
Estimates time or space complexity for an operation. 
Supports O(1), O(N), and O(N^2).
"""


# TODO add O(log(N)) and O(N*log(N))

class ComplexityAnalyzer:
    def __init__(self, plot=False, default_num_runs=10_000, default_num_tests=5, default_error_threshold=0.05,
                 default_coef_threshold=0.000001):
        """
        Create complexity analyzer
        :param plot: true to plot values against expected
        :param default_num_runs: default number of runs per test (can be overridden in analyze methods)
        :param default_num_tests: default number of tests (can be overridden in analyze methods)
        :param default_error_threshold: default threshold (minimum proportion of error used to select higher level)
        :param default_coef_threshold: default threshold to ignore coefficients
        """
        self.plot = plot
        self.default_num_runs = default_num_runs
        self.default_num_tests = default_num_tests
        self.default_error_threshold = default_error_threshold
        self.default_coef_threshold = default_coef_threshold

    def analyze_time(self, op, title=None, init_test=None, init_op=None, post_op=None,
                     num_runs=None, num_tests=None, error_threshold=None, coef_threshold=None):
        """
        Estimates space complexity for the given operation.
        :param op: operation to test (function with run number arguments)
        :param title: title to print with plot (ignored if plot not enabled)
        :param init_test: initialize collection before each test (function with test number arguments)
        :param init_op: initialize operation (function with run number argument)
        :param post_op: cleanup after operation (function with run number argument)
        :param num_tests number of tests to run, or None to use the class default
        :param num_runs number of runs per test (not including initial non-measured run), or None to use the class default
        :param error_threshold: threshold (minimum proportion of error used to select higher level), or None to use the class default
        :param coef_threshold: threshold to ignore coefficients, or None to use the class default
        """
        return self.analyze(
            op,
            metric=lambda _: time.perf_counter_ns(),
            absolute_metric=False,
            title=title,
            y_axis='Time',
            init_test=init_test,
            init_op=init_op,
            post_op=post_op,
            num_runs=num_runs,
            num_tests=num_tests,
            error_threshold=error_threshold,
            coef_threshold=coef_threshold,
        )

    def analyze_space(self, op, get_estimated_space, title=None, init_test=None, init_op=None, post_op=None,
                      num_runs=None, num_tests=None, error_threshold=None, coef_threshold=None):
        """
        Estimates space complexity for the given operation.
        :param op: operation to test (function with run number argument)
        :param get_estimated_space: no-arg function to get the current space
        :param title: title to print with plot (ignored if plot not enabled)
        :param init_test: initialize collection before each test (function with test number arguments)
        :param init_op: initialize operation (function with run number argument)
        :param post_op: cleanup after operation (function with run number argument)
        :param num_tests number of tests to run, or None to use the class default
        :param num_runs number of runs per test (not including initial non-measured run), or None to use the class default
        :param error_threshold: threshold (minimum proportion of error used to select higher level), or None to use the class default
        :param coef_threshold: threshold to ignore coefficients, or None to use the class default
        """
        result = self.analyze(
            op,
            metric=lambda _: get_estimated_space(),
            absolute_metric=True,
            title=title,
            y_axis='Space',
            init_test=init_test,
            init_op=init_op,
            post_op=post_op,
            num_runs=num_runs,
            num_tests=num_tests,
            error_threshold=error_threshold,
            coef_threshold=coef_threshold,
        )

        return result

    def analyze(self, op, metric, absolute_metric, title=None, y_axis=None, init_test=None, init_op=None, post_op=None,
                num_runs=None, num_tests=None, error_threshold=None, coef_threshold=None):
        """
        Estimates complexity for the given operation.
        :param metric: metric to test (function with no arguments that returns a numeric value)
        :param absolute_metric: true if the metric represents an absolute value such as a size rather than a relative value such as a timestamp
        :param op: command to test (function with run number arguments)
        :param title: title to print with plot (ignored if plot not enabled)
        :param y_axis: name of y-axis (ignored if plot not enabled)
        :param init_test: initialize collection before each test (function with test number arguments)
        :param init_op: initialize operation (function with run number argument)
        :param post_op: cleanup after operation (function with run number argument)
        :param num_tests number of tests to run, or None to use the class default
        :param num_runs number of runs per test (not including initial non-measured run), or None to use the class default
        :param error_threshold: threshold (minimum proportion of error used to select higher level), or None to use the class default
        :param coef_threshold: threshold to ignore coefficients, or None to use the class default
        """
        metrics = [0] * num_runs

        if num_tests is None:
            num_tests = self.default_num_tests
        if num_runs is None:
            num_runs = self.default_num_runs
        if error_threshold is None:
            error_threshold = self.default_error_threshold
        if coef_threshold is None:
            coef_threshold = self.default_coef_threshold

        for test in range(num_tests):
            if init_test:
                init_test(test + 1)

            metric_adjustment = 0  # adjustment for any changes in init_op for absolute metrics

            # do an additional first run that is ignored for metrics
            for run in range(num_runs + 1):
                if init_op:
                    if absolute_metric:
                        # ignore metric changes in init_op for absolute metrics like size
                        pre_init_metric = metric(run)
                        init_op(run)
                        metric_adjustment += metric(run) - pre_init_metric
                    else:
                        init_op(run)

                start_metric = metric(run) if run > 0 and not absolute_metric else 0
                op(run)
                if run > 0:
                    # skip metric for first run
                    new_metric = metric(run) - start_metric - metric_adjustment
                    metrics[run - 1] = new_metric
                if post_op:
                    post_op(run)

        x = [i + 1 for i in range(len(metrics))]

        def get_level(x_transformed, degree, level_name):
            coef = np.polyfit(x_transformed, metrics, degree)
            fit = np.poly1d(coef)
            y_pred = fit(x_transformed)
            return np.sqrt(np.mean((metrics - y_pred) ** 2)), x_transformed, y_pred, coef, level_name

        # O(N^2)
        level_n_2 = get_level(x, 2, 'O(N^2)')

        # TODO fix log (may work now)
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

        def check_error_threshold(error, remaining_levels):
            return error * (1 + error_threshold) < min(map(lambda level: level[0], remaining_levels))

        def is_best_level(error, coef, remaining_levels):
            return abs(coef[0]) > coef_threshold and check_error_threshold(error, remaining_levels)

        for run, (error, level_x, level_y, coef, level_name) in enumerate(levels):
            if run == len(levels) - 1 or is_best_level(error, coef, levels[run + 1:]):
                if self.plot:
                    print(level_name)
                    fig, ax = plt.subplots()

                    ax.plot(x, metrics, label='Actual')
                    ax.plot(level_x, level_y, label=f'Estimated')

                    ax.set_xlabel('Runs')
                    ax.set_ylabel(y_axis)
                    ax.legend()

                    subtitle = f'{title} {level_name}' if title else level_name
                    plt.suptitle(subtitle)
                    plt.tight_layout()
                    plt.show()
                return level_name

    def execute(self, collection, collection_type):
        """
        Execute complexity analyzer mode.
        See CollectionInterface for collection requirements.
        :param collection: collection instance
        :param collection_type: collection type, e.g. 'Linked List'
        """
        while True:
            print('--------------------------------------------------------------')
            print('Enter complexity analyzer command:')
            print('  ta) Analyze time complexity to add')
            print('  tr) Analyze time complexity to remove')
            print('  ts) Analyze time complexity to search for random element')
            print('  sa) Analyze space complexity to add')
            print('  sr) Analyze space complexity to remove')
            print('  ss) Analyze space complexity to search for random element')
            print('  q) Quit complexity analyzer mode')
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

                self.analyze_time(op, title=f'{collection_type} Add Time Complexity', init_test=init_test,
                                  num_runs=2_000)
            elif cmd == 'tr':
                # analyze time complexity for remove
                num_runs = 2_000

                def init_test(_):
                    collection.clear()
                    # populate with number of runs, including initial extra run
                    for i in range(num_runs + 1):
                        collection.push(random.random())

                def op(_):
                    collection.pop()

                self.analyze_time(op, title=f'{collection_type} Remove Time Complexity', init_test=init_test,
                                  num_runs=num_runs)
            elif cmd == 'ts':
                # analyze time complexity for search

                def init_test(_):
                    collection.clear()

                def init_op(i):
                    # add next item
                    collection.push(i)

                def op(_):
                    collection.index(random.randint(0, len(collection) - 1))

                self.analyze_time(op, title=f'{collection_type} Add Space Complexity', init_test=init_test,
                                  init_op=init_op, num_runs=2_000)
            elif cmd == 'sa':
                # analyze space complexity for add
                num_runs = 20

                def init_test(_):
                    collection.clear()

                def op(_):
                    collection.push(len(collection))

                def get_estimated_space():
                    return collection.get_estimated_space()

                self.analyze_space(op, get_estimated_space, title=f'{collection_type} Add Space Complexity',
                                   init_test=init_test, num_runs=num_runs)
            elif cmd == 'sr':
                # analyze space complexity for remove
                num_runs = 20

                def init_test(_):
                    # start with full collection (including extra initial run)
                    collection.clear()
                    for _ in range(num_runs + 1):
                        collection.push(0)

                def op(_):
                    collection.pop()

                def get_estimated_space():
                    return collection.get_estimated_space()

                self.analyze_space(op, get_estimated_space, title=f'{collection_type} Remove Space Complexity',
                                   init_test=init_test, num_runs=num_runs)
            elif cmd == 'ss':
                # analyze space complexity for search
                num_runs = 20

                def init_test(_):
                    collection.clear()

                def init_op(i):
                    # not included in metric
                    collection.push(i)

                def op(_):
                    collection.index(random.randint(0, len(collection) - 1))

                def get_estimated_space():
                    return collection.get_estimated_space()

                self.analyze_space(op, get_estimated_space, title=f'{collection_type} Search Space Complexity',
                                   init_test=init_test, init_op=init_op, num_runs=num_runs)
            else:
                print('Invalid command')
