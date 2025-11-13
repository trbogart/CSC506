import gc
import random

import numpy as np
import tracemalloc
import time

"""
Estimates time or space complexity for an operation. 
Supports O(1), O(N), and O(N^2).
TODO: O(log(N)) and O(N*log(N))
"""
class ComplexityAnalyzer:
    default_num_iterations = 10_000
    default_num_tests = 5
    default_threshold = 0.05

    def analyze_time(self, init_test, init_op, op, num_iterations = default_num_iterations, num_tests = default_num_tests, threshold = default_threshold):
        return self.analyze(lambda: time.perf_counter_ns(), init_test, init_op, op, num_iterations, num_tests, threshold)

    @staticmethod
    def analyze_memory(self, init_test, init_op, op, num_iterations = default_num_iterations, num_tests = default_num_tests, threshold = default_threshold):
        def get_memory_usage():
            gc.collect()
            current, _ = tracemalloc.get_traced_memory()
            return current

        tracemalloc.start()
        result = self.analyze(lambda: get_memory_usage(), init_test, init_op, op, num_iterations, num_tests, threshold)
        tracemalloc.stop()
        return result

    def analyze(self, metric, init_test, init_op, op, num_iterations = default_num_iterations, num_tests = default_num_tests, threshold = default_threshold):
        """
        Estimates time complexity for the given operation.
        :param metric: metric to test (function with no arguments that returns a numeric value)
        :param init_test: initialize collection before each test (function with num_iterations argument)
        :param init_op: initialize operation (function with index argument, not included in metric)
        :param op: operation to test (function with index arguments)
        :param num_iterations number of iterations to test
        :param num_tests number of tests to run
        :param threshold: threshold % required to accept higher order
        """
        metrics = [0] * num_iterations

        for test in range(num_tests):
            init_test(num_iterations)
            for i in range(num_iterations):
                init_op(i)
                start_metric = metric()
                op(i)
                end_metric = metric()
                metrics[i] += end_metric - start_metric

        x = [i+1 for i in range(num_iterations)]

        def get_error(x, degree):
            coef = np.polyfit(x, metrics, degree)
            fit = np.poly1d(coef)
            y_pred = fit(x)
            return np.sqrt(np.mean((metrics - y_pred) ** 2))

        # O(N^2)
        error_quadratic = get_error(x, 2)

        # O(N)
        error_linear = get_error(x, 1)

        # O(1)
        error_constant = get_error(x, 0)

        # TODO fix log
        # # O(N * log(N))
        # x_n_log = np.log(x) * x
        # error_n_log = get_error(x_n_log, 1)
        # errors_and_complexities.append((error_n_log, 'O(N*log(N))'))
        #
        # # O(log(N))
        # x_log = np.log(x)
        # error_log = get_error(x_log, 1)
        # errors_and_complexities.append((error_log, 'O(log(N))'))

        errors_and_complexities = [
            (error_quadratic, 'O(N^2)'),
            # (error_n_log, 'O(N*log(N))') # TODO fix log
            (error_linear, 'O(N)'),
            # (error_log, 'O(log(N))') # TODO fix log
            (error_constant, 'O(1)'),
        ]

        # find complexity with highest level where error of next lower level is at least threshold % higher
        error_threshold = 1 + threshold

        for i, (error, name) in enumerate(errors_and_complexities):
            if i == len(errors_and_complexities) - 1 or error * error_threshold < min(map(lambda ec: ec[0], errors_and_complexities[i+1:])):
                print(name)
                return name

    def execute(self, collection):
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
                def init_test(_):
                    collection.clear()

                def init_op(_):
                    pass

                def op(_):
                    collection.push(random.random())

                self.analyze_time(init_test, init_op, op)
            elif cmd == 'tr':
                def init_test(num_iterations):
                    collection.clear()
                    for i in range(num_iterations):
                        collection.push(random.random())

                def init_op(_):
                    pass

                def op(_):
                    collection.push(random.random())

                self.analyze_time(init_test, init_op, op)
            elif cmd == 'ts':
                elements = [random.random() for _ in range(self.num_iterations)]

                def init_test(_):
                    collection.clear()

                def init_op(i):
                    collection.push(elements[i])

                def op(i):
                    collection.index(elements[random.randint(0, i-1)])

                self.analyze_time(init_test, init_op, op)
            else:
                print('Invalid command')










