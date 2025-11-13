import gc
import random

import numpy as np
import tracemalloc
import time

"""
Analyze time or space complexity for an operation
"""
class Analyzer:
    num_iterations = 200
    num_tests = 5
    default_threshold = 0.1

    @staticmethod
    def analyze_time(init_test, init_op, op, num_iterations = num_iterations, num_tests = num_tests, threshold = default_threshold):
        Analyzer.analyze('time', lambda: time.perf_counter_ns(), init_test, init_op, op, num_iterations, num_tests, threshold)

    @staticmethod
    def analyze_memory(init_test, init_op, op, num_iterations = num_iterations, num_tests = num_tests, threshold = default_threshold):
        def get_memory_usage():
            gc.collect()
            current, _ = tracemalloc.get_traced_memory()
            return current

        tracemalloc.start()
        Analyzer.analyze('memory', lambda: get_memory_usage(), init_test, init_op, op, num_iterations, num_tests, threshold)
        tracemalloc.stop()

    @staticmethod
    def analyze(metric_name, metric, init_test, init_op, op, num_iterations, num_tests, threshold = default_threshold):
        """
        Estimates time complexity (constant, linear, or quadratic) for the given operation.
        :param metric_name: name of the metric to analyze
        :param metric: metric to test (function with no arguments that returns a numeric value)
        :param init_test: initialize collection before each test (function with no arguments)
        :param init_op: initialize operation (function with index argument, not included in metric)
        :param op: operation to test (function with index arguments)
        :param num_iterations: number of times to repeat the operation for each test
        :param num_tests: number of tests to run
        :param threshold: improvement threshold to accept degree
        """
        metrics = [0] * num_iterations

        for test in range(num_tests):
            init_test()
            for i in range(num_iterations):
                init_op(i)
                start_metric = metric()
                op(i)
                end_metric = metric()
                metrics[i] += end_metric - start_metric

        x = [i for i in range(num_iterations)]

        def get_error(degree):
            coef = np.polyfit(x, metrics, degree)
            y_pred = np.polyval(coef, x)
            return np.sqrt(np.mean((metrics - y_pred) ** 2))

        # quadratic
        error2 = get_error(2)

        # linear
        error1 = get_error(1)

        # constant
        error0 = get_error(0)

        # TODO support n*log(n) and log(n)
        # x_transformed = np.log(x) # or x * np.log(x)
        # coef = np.polyfit(x_transformed, metrics, 1)
        # fit = np.poly1d(coef)
        # y_pred = fit(x_transformed)

        if error2 * (1 + threshold) < min(error1, error0):
            print('O(n^2)')
        elif error1 * (1 + threshold) < error0:
            print('O(n)')
        else:
            print('O(1)')

    @staticmethod
    def execute(collection):
        while True:
            print('--------------------------------------------------------------')
            print('Enter command:')
            print('  ta) Analyze time complexity to add' )
            print('  tr) Analyze time complexity to remove' )
            print('  ts) Analyze time complexity to search for random element' )
            print('  sa) Analyze space complexity to add' )
            print('  sr) Analyze space complexity to remove' )
            print('  ss) Analyze space complexity to search for random element' )
            print('  q) Quit')
            cmd = input('> ')

            if cmd == 'q':
                collection.clear()
                return
            elif cmd == 'ta':
                def init_test():
                    collection.clear()

                def init_op(_):
                    pass

                def op(_):
                    collection.push(random.random())

                Analyzer.analyze_time(init_test, init_op, op)
            elif cmd == 'tr':
                def init_test():
                    collection.clear()
                    for i in range(Analyzer.num_iterations):
                        collection.push(random.random())

                def init_op(_):
                    pass

                def op(_):
                    collection.push(random.random())

                Analyzer.analyze_time(init_test, init_op, op)
            elif cmd == 'ts':
                elements = [random.random() for i in range(Analyzer.num_iterations)]

                def init_test():
                    collection.clear()

                def init_op(i):
                    collection.push(elements[i])

                def op(i):
                    collection.index(elements[random.randint(0, i)])

                Analyzer.analyze_time(init_test, init_op, op)
            else:
                print('Invalid command')










