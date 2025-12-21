from os.path import basename
from random import shuffle
from sys import argv
from time import perf_counter

from matplotlib import pyplot as plt

from module6.binary_search_tree import BinarySearchTree

if __name__ == '__main__':
    bst = BinarySearchTree()
    a = []
    ht = {}
    keys = [i for i in range(1000)]
    shuffle(keys)

    def _perf(data_type, data, insert_op, search_op):
        all_test_metrics = []
        insert_op(1)
        search_op(1)

        num_tests = 3
        for _ in range(num_tests):
            data.clear()
            test_metrics = []
            all_test_metrics.append(test_metrics)
            shuffle(keys)
            for test_index, key in enumerate(keys):
                insert_op(key)
                start_time = perf_counter()
                search_op(key)
                test_metrics.append(perf_counter() - start_time)
            assert len(data) == len(data)

        median_metrics = []
        for i in range(len(keys)):
            iteration_metrics = []
            for test_metrics in all_test_metrics:
                iteration_metrics.append(test_metrics[i])
            iteration_metrics.sort()
            median_metrics.append(iteration_metrics[len(iteration_metrics) // 2])

        x = [i + 1 for i in range(len(keys))]

        title = f'{data_type} Search'
        plt.gcf().set_size_inches(9, 3.5)
        plt.plot(x, median_metrics)
        plt.title(title)
        plt.xlabel('Size')
        plt.ylabel('Time (s)')
        plt.savefig(f'{title}.png')
        plt.show()

    _perf('Binary Search Tree', bst, bst.insert, bst.search)
    _perf('Linear', a, a.append, a.index)
    def update_ht(key):
        ht[key] = key
    _perf('Hashtable', ht, update_ht, ht.__getitem__)
