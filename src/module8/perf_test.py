from abc import ABC, abstractmethod
from dataclasses import dataclass
from random import randint, shuffle, random
from time import perf_counter
from typing import Callable

import numpy as np
from matplotlib import pyplot as plt

from module8.bubble_sort import bubble_sort
from module8.collection import Collection, OrderedCollection
from module8.graph import Graph
from module8.graph_adjacency_list import GraphAdjacencyList
from module8.hash_table import HashTable
from module8.linked_list import LinkedList
from module8.queue import Queue
from module8.sort import insertion_sort
from module8.stack import Stack
from module8.tree import BinarySearchTree


@dataclass
class PerfTestResults:
    """
    Wrapper for performance test results, including estimated complexity.

    Attributes:
        operation (str): The name of the test (e.g. binary search)
        sizes (ndarray): Sizes that were tested for eac operation
        metrics (ndarray): Actual times to add at each size
    """
    operation: str
    sizes: np.ndarray
    metrics: np.ndarray


class PerfTest(ABC):
    """
    Abstract base class to define a test that will run a performance test on an operation at different sizes
    and estimate the time complexity.
    """

    default_num_runs = 10

    """
    Defines a single performance test, e.g. searching a binary tree.
    """

    def __init__(self, operation: str):
        """
        Initialize the test.
        :param operation: The name of the test, e.g. binary search
        """
        self.operation = operation

    @abstractmethod
    def init_run(self, size: int):
        """
        Initialize data before each test run, not included in performance metrics.
        This method may be called multiple times at the same size, but the size will never decrease.
        :param size: size of the data to operate on
        """
        pass

    @abstractmethod
    def run(self):
        """
        Executes a single run of the test.
        """
        pass

    def execute(self, sizes: list[int], num_runs: int = default_num_runs) -> PerfTestResults:
        """
        Tests performance at difference sizes
        :return: performance results
        """

        metrics = []
        for size in sizes:
            size_metrics = []
            # run once at each size without gathering metrics
            for run in range(num_runs + 1):
                self.init_run(size)
                start_time = perf_counter()
                self.run()
                if run > 0:
                    size_metrics.append(perf_counter() - start_time)
            metrics.append(self._get_median(size_metrics))

        return PerfTestResults(self.operation, np.array(sizes), np.array(metrics))

    @staticmethod
    def _get_median(times: list[float]) -> float:
        """
        Returns the mean of the middle third of the data.
        :param times: array of values
        :return: the mean of the middle third of the data
        """
        num_runs = len(times)
        if num_runs > 2:
            times.sort()
            drop_times = num_runs // 3
            times = times[drop_times:-drop_times]
        return sum(times) / len(times)


class PerfTestCollectionContains(PerfTest):
    """
    Test performance for checking if an element is in a collection.
    """

    def __init__(self, operation: str, collection: Collection[int]):
        PerfTest.__init__(self, operation)
        self.collection = collection

    def init_run(self, size: int):
        if size != len(self.collection):
            self.collection.clear()

            # randomize data)
            data = [i + 1 for i in range(size)]
            shuffle(data)
            for value in data:
                self.collection.add(value)

    def run(self):
        # lookup random value in hashtable
        _ = randint(1, len(self.collection)) in self.collection


class PerfTestRemoveLast(PerfTest):
    """
    Test performance for removing the last item in an ordered collection.
    """

    def __init__(self, collection_type: str, collection: OrderedCollection[int]):
        PerfTest.__init__(self, f'Remove Last from {collection_type}')
        self.collection = collection

    def init_run(self, size: int):
        if size != len(self.collection):
            self.collection.clear()
            for i in range(size):
                self.collection.add(i)

    def run(self):
        self.collection.remove_last()


class PerfTestRemoveFirst(PerfTest):
    """
    Test performance for removing the first item in an ordered collection.
    """

    def __init__(self, collection_type: str, collection: OrderedCollection[int]):
        PerfTest.__init__(self, f'Remove First from {collection_type}')
        self.collection = collection

    def init_run(self, size: int):
        if size != len(self.collection):
            self.collection.clear()
            for i in range(size):
                self.collection.add(i)

    def run(self):
        self.collection.remove_first()


class PerfTestSort(PerfTest):
    def __init__(self, operation: str, sort_op: Callable[[list[int]], None], shuffled: bool):
        PerfTest.__init__(self, operation)
        self.data = []
        self.sort_op = sort_op
        self.shuffled = shuffled

    def init_run(self, size: int):
        if size != len(self.data):
            self.data = [i + 1 for i in range(size)]
        if self.shuffled:
            shuffle(self.data)

    def run(self):
        self.sort_op(self.data)


class PerfTestShortestPath(PerfTest):
    def __init__(self, name: str, graph: Graph):
        PerfTest.__init__(self, name)
        self.graph = graph
        self.vertices = []

    def init_run(self, size: int):
        while size > len(self.graph.vertices):
            new_vertex = self.graph.add_vertex(f'v{len(self.graph.vertices) + 1}')

            for vertex in self.vertices:
                # 10% chance of any 2 vertices being connected (no cycles)
                if random() < .1:
                    weight = randint(1, 5)
                    self.graph.add_edge(vertex, new_vertex, weight)

            self.vertices.append(new_vertex)

    def run(self):
        self.graph.shortest_path(self.vertices[0], self.vertices[-1])


def execute_tests(title: str, tests: list[PerfTest], sizes: list[int], log_x: bool = False, log_y: bool = False,
                  num_runs: int = PerfTest.default_num_runs):
    results = []
    for test in tests:
        print(f'Executing {title} - {test.operation}...')
        results.append(test.execute(sizes, num_runs))

    fig, ax = plt.subplots(figsize=(6, 3.3))

    if log_x:
        x = np.log2(sizes)
        x_label = 'Log₂ Size'
    else:
        x = sizes
        x_label = 'Size'

    if log_y:
        y_label = 'Log₂ Time'
    else:
        y_label = 'Time'

    for result in results:
        if log_y:
            y = np.log2(result.metrics)
        else:
            y = result.metrics
        ax.plot(x, y, label=result.operation)

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.legend()
    plt.tight_layout()
    plt.suptitle(title)
    plt.show()


def perf_test():
    sizes = [2 ** i for i in range(5, 12)]  # [32, 64, 128, 256, 512, 1024, 2048]
    search_tests = [
        PerfTestCollectionContains('Hash Table', HashTable()),
        PerfTestCollectionContains('Binary Search Tree', BinarySearchTree()),
        PerfTestCollectionContains('Linked List', LinkedList()),
    ]
    execute_tests('Collection Lookup', search_tests, sizes, num_runs=200, log_y=True)

    remove_first_last_tests = [
        PerfTestRemoveLast("Stack", Stack()),
        PerfTestRemoveLast("Queue", Queue()),
        PerfTestRemoveFirst("Stack", Stack()),
        PerfTestRemoveFirst("Queue", Queue()),
    ]
    execute_tests('Remove First/Last', remove_first_last_tests, sizes, num_runs=200)

    sort_tests = [
        PerfTestSort('Insertion Sort (Sorted)', insertion_sort, shuffled=False),
        PerfTestSort('Insertion Sort (Shuffled)', insertion_sort, shuffled=True),
        PerfTestSort('Bubble Sort (Shuffled)', bubble_sort, shuffled=True),
    ]
    execute_tests('Sort Algorithms', sort_tests, sizes)

    shortest_path_tests = [
        PerfTestShortestPath('Adjacency List', GraphAdjacencyList()),
    ]

    execute_tests('Shortest Path', shortest_path_tests, sizes)


if __name__ == '__main__':
    perf_test()
