import random
from time import perf_counter

from module6.binary_search_tree import BinarySearchTree
from module8.bubble_sort import bubble_sort
from module8.collection import OrderedCollection
from module8.perf_test import perf_test
from module8.queue import Queue
from module8.quickselect import quickselect
from module8.set import Set
from module8.sort import insertion_sort, merge_sort
from module8.stack import Stack


class ConsoleInterface:
    """
    Console interface for testing collections and algorithms.
    """

    def __init__(self):
        self.collection = Stack()

    def use_stack(self):
        self.collection = Stack()

    def use_queue(self):
        self.collection = Queue()

    def use_set(self):
        self.collection = Set()

    def use_tree(self):
        self.collection = BinarySearchTree()

    def add(self, value):
        self.collection.add(value)

    def populate_data(self, size, shuffled):
        self.collection.clear()
        data = [i + 1 for i in range(size)]
        if shuffled:
            random.shuffle(data)
        for value in data:
            self.collection.add(value)

    def list_elements(self):
        size = len(self.collection)
        if size == 0:
            print('List is empty')
        else:
            for i, element in enumerate(self.collection):
                print(f'[{i}]: {element}')

    def execute(self):
        print_menu = True
        while True:
            try:
                print('-' * 80)
                if type(self.collection) == Stack:
                    collections_type = 'Stack (Array List)'
                elif type(self.collection) == Queue:
                    collections_type = 'Queue (Linked List)'
                elif type(self.collection) == Set:
                    collections_type = 'Set (Hash Table)'
                elif type(self.collection) == BinarySearchTree:
                    collections_type = 'Binary Search Tree'
                else:
                    assert False
                print(f'{collections_type} with {len(self.collection)} elements')

                if print_menu:
                    print('q: Quit')
                    print('m: Print this menu')
                    print('st: Use stack (array list)')
                    print('q: Use queue (linked list)')
                    print('set: Use hash set')
                    print('tree: Use binary search tree')
                    print('add: Add element')
                    print('rem: Remove element')
                    print('pop: Populate elements (set size and/or shuffle)')
                    print('ls: List elements')
                    print('bs: Bubble sort (stack only)')
                    print('is: Insertion sort (stack only)')
                    print('ms: Merge sort (stack only)')
                    print('qs: Quickselect (stack only)')
                    print('int: Intersection (set only)')
                    print('un: Union (set only)')
                    print('diff: Difference (set only)')
                    print('sd: Symmetric difference (set only)')
                    print('perf: Performance comparisons')
                    print_menu = False

                cmd = input('Enter command (q to quit or m to print menu)> ')
                if cmd == 'q':
                    break
                elif cmd == 'm':
                    print_menu = True
                elif cmd == 'st':
                    self.use_stack()
                elif cmd == 'q':
                    self.use_queue()
                elif cmd == 'set':
                    self.use_set()
                elif cmd == 'tree':
                    self.use_tree()
                elif cmd == 'add':
                    value = input('Enter value: ')
                    self.collection.add(value)
                elif cmd == 'rem':
                    if isinstance(self.collection, OrderedCollection):
                        value = self.collection.remove_next()
                        print(f'Removed {value}')
                    else:
                        value = input('Value to remove: ')
                        if self.collection.remove(value):
                            print(f'Removed {value}')
                        else:
                            print(f'Did not remove {value}')
                elif cmd == 'pop':
                    size = int(input('Enter size: '))
                    shuffled = int(input('Enter 0 for sorted data or 1 for shuffled data: '))
                    self.populate_data(size, shuffled == 1)
                elif cmd == 'ls':
                    print('Values:')
                    for i, value in enumerate(self.collection):
                        print(f'[{i}] {value}')
                elif cmd == 'bs':
                    if type(self.collection) == Stack:
                        print('Running bubble sort...')
                        start_time = perf_counter()
                        bubble_sort(self.collection.list)
                    else:
                        print("Sorting only supported for stack (array list)")
                elif cmd == 'is':
                    if type(self.collection) == Stack:
                        print('Running insertion sort...')
                        start_time = perf_counter()
                        insertion_sort(self.collection.list)
                        print(f'Finished in {perf_counter() - start_time:.3f} seconds')
                    else:
                        print("Sorting only supported for stack (array list)")
                elif cmd == 'ms':
                    if type(self.collection) == Stack:
                        print('Running merge sort...')
                        start_time = perf_counter()
                        merge_sort(self.collection.list)
                        print(f'Finished in {perf_counter() - start_time:.3f} seconds')
                    else:
                        print("Sorting only supported for stack (array list)")
                elif cmd == 'qs':
                    if type(self.collection) == Stack:
                        k = int(input('Enter k (0 for smallest element, 1 for 2nd smallest element, etc.): '))
                        if 0 <= k < len(self.collection):
                            print('Running quickselect...')
                            start_time = perf_counter()
                            value = quickselect(self.collection.list, k)
                            print(f'Finished in {perf_counter() - start_time:.3f} seconds')
                            print(f'Result: {value}')
                        else:
                            print('Invalid value')
                    else:
                        print("Quickselect only supported for stack (array list)")
                elif cmd == 'perf':
                    perf_test()
                elif cmd == 'int':
                    if type(self.collection) == Set:
                        values = input(f'Enter values to take intersection on: ').split()
                        other_set = Set()
                        for value in values:
                            other_set.add(value)
                        result = self.collection.intersection(other_set)
                        print(f'Result: {', '.join(result)}')
                    else:
                        print('Intersection only supported for sets')
                elif cmd == 'union':
                    if type(self.collection) == Set:
                        values = input(f'Enter values to take union on: ').split()
                        other_set = Set()
                        for value in values:
                            other_set.add(value)
                        print(f'??? other_set: {other_set}')
                        print()
                        result = self.collection.union(other_set)
                        print(f'Result: {', '.join(result)}')
                    else:
                        print('Union only supported for sets')
                elif cmd == 'diff':
                    if type(self.collection) == Set:
                        values = input(f'Enter values to take difference on: ').split()
                        other_set = Set()
                        for value in values:
                            other_set.add(value)
                        result = self.collection.difference(other_set)
                        print(f'Result: {', '.join(result)}')
                    else:
                        print('Difference only supported for sets')
                elif cmd == 'sd':
                    if type(self.collection) == Set:
                        values = input(f'Enter values to take symmetric difference on: ').split()
                        other_set = Set()
                        for value in values:
                            other_set.add(value)
                        result = self.collection.symmetric_difference(other_set)
                        print(f'Result: {', '.join(result)}')
                    else:
                        print('Symmetric difference only supported for sets')
                else:
                    print('Invalid command, try again')
            except Exception as e:
                print(f'Invalid command, try again: {e}')


if __name__ == '__main__':
    ConsoleInterface().execute()
