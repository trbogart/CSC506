from random import shuffle
from time import perf_counter
import matplotlib.pyplot as plt

from module6.binary_search_tree import BinarySearchTree, TraversalOrder


class BinarySearchTreeTester:
    def __init__(self):
        self.bst = BinarySearchTree()

    def __str__(self):
        return f'BST with {self.bst.size} elements, {self.bst.get_height()} height, {self.bst.get_balanced_height()} min height, {len(self.bst)-1} max height'

    def add(self, element):
        self.bst.insert(element)

    def search(self, element):
        if self.bst.search(element) is None:
            print("Element not found")
        else:
            print("Element found")

    def delete(self, element):
        if self.bst.delete(element) is None:
            print("Element not deleted")
        else:
            print("Element deleted")

    def print_tree(self):
        print(self.bst)

    def check_balance(self):
        print(f'Balance factor is {self.bst.get_balance_factor()} (min is {self.bst.get_balanced_height()}, max is {len(self.bst) - 1}')

    def list(self, order):
        print(f'Listing {len(self.bst)} elements')
        for i, e in enumerate(self.bst.traverse(order)):
            print(f'[{i}] {e}')

    def min(self):
        print(f'Min value: {self.bst.get_min_value()}')

    def max(self):
        print(f'Max value: {self.bst.get_max_value()}')

    def randomize(self):
        values = [e for e in self.bst]
        self.bst.clear()
        shuffle(values)
        for value in values:
            self.bst.insert(value)

    def clear(self):
        self.bst.clear()

    def perf(self):
        bst = BinarySearchTree()
        a = []
        keys = [i for i in range(1000)]
        shuffle(keys)

        def _perf(data_type, data, insert_op, search_op):
            all_test_metrics = []
            insert_op(1)
            search_op(1)

            num_tests = 5
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

            plt.plot(x, median_metrics)
            plt.title(f'{data_type} Search')
            plt.xlabel('Size')
            plt.ylabel('Time (s)')
            plt.show()

        _perf('BST', bst, bst.insert, bst.search)
        _perf('Linear', a, a.append, a.index)


if __name__ == '__main__':
    tester = BinarySearchTreeTester()

    def print_menu():
        print('Menu:')
        print('a) Add element')
        print('s) Search for element')
        print('d) Delete element')
        print('p) Print tree')
        print('b) Check balance')
        print('r) Randomize tree')
        print('in) In-order traversal')
        print('pre) Pre-order traversal')
        print('post) Post-order traversal')
        print('min) Minimum value')
        print('max) Maximum value')
        print('perf) Performance testing')
        print('c) Clear')
        print('m) Print menu')
        print('q) Quit')

    print_menu()
    while True:
        cmd = input(f'Enter command for {tester} (m to print menu, q to quit): ')
        if cmd == 'a':
            element = input('Enter element to add: ')
            tester.add(element)
        elif cmd == 's':
            element = input('Enter element to search: ')
            tester.search(element)
        elif cmd == 'd':
            element = input('Enter element to delete: ')
            tester.delete(element)
        elif cmd == 'p':
            tester.print_tree()
        elif cmd == 'b':
            tester.check_balance()
        elif cmd == 'r':
            tester.randomize()
        elif cmd == 'in':
            tester.list(TraversalOrder.IN_ORDER)
        elif cmd == 'pre':
            tester.list(TraversalOrder.PRE_ORDER)
        elif cmd == 'post':
            tester.list(TraversalOrder.POST_ORDER)
        elif cmd == 'min':
            tester.min()
        elif cmd == 'max':
            tester.max()
        elif cmd == 'perf':
            tester.perf()
        elif cmd == 'c':
            tester.clear()

        elif cmd == 'm':
            print_menu()
        elif cmd == 'q':
            break
        else:
            print('Invalid command')