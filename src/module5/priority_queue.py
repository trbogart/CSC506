import random
from time import perf_counter

from matplotlib import pyplot as plt


class PriorityQueue[T]:
    """
    Priority queue implemented using a min heap.
    """

    class ValueWithPriority:
        def __init__(self, value: T, priority: int):
            self.value = value
            self.priority = priority

        def __repr__(self):
            return f'{repr(self.value)}: {self.priority}'

    def __init__(self):
        self.min_heap = []

    def __len__(self) -> int:
        return len(self.min_heap)

    def push(self, value: T, priority: int) -> None:
        self.min_heap.append(self.ValueWithPriority(value, priority))
        self._move_up(len(self.min_heap) - 1)

    def pop(self) -> tuple[T, int]:
        if len(self.min_heap) == 0:
            raise IndexError('Priority queue is empty')
        if len(self.min_heap) == 1:
            vwp = self.min_heap.pop()
            return vwp.value, vwp.priority

        # swap first and last entries
        last_index = len(self.min_heap) - 1
        self.min_heap[0], self.min_heap[last_index] = self.min_heap[last_index], self.min_heap[0]

        # pop last element and move head to correct location
        vwp = self.min_heap.pop()
        self._move_down(0)
        return vwp.value, vwp.priority

    def peek(self) -> tuple[T, int]:
        if len(self.min_heap) == 0:
            raise IndexError('Priority queue is empty')
        vwp = self.min_heap[0]
        return vwp.value, vwp.priority

    def _move_up(self, index: int) -> None:
        while index != 0:
            parent_index = (index - 1) // 2
            if self.min_heap[index].priority < self.min_heap[parent_index].priority:
                # swap with parent and repeat
                self.min_heap[index], self.min_heap[parent_index] = self.min_heap[parent_index], self.min_heap[index]
                index = parent_index
            else:
                break

    def _move_down(self, index: int) -> None:
        while True:
            left_index = index * 2 + 1
            if left_index < len(self.min_heap):
                min_index = index
                min_priority = self.min_heap[index].priority
                if self.min_heap[left_index].priority < min_priority:
                    min_index = left_index
                    min_priority = self.min_heap[left_index].priority

                right_index = left_index + 1
                if right_index < len(self.min_heap) and self.min_heap[right_index].priority < min_priority:
                    min_index = right_index

                if min_index == index:
                    # in correct location
                    break
                else:
                    # swap with smaller child and repeat
                    self.min_heap[index], self.min_heap[min_index] = self.min_heap[min_index], self.min_heap[index]
                    index = min_index
            else:
                # leaf node
                break


if __name__ == '__main__':
    pq = PriorityQueue()
    push_metrics = []
    pop_metrics = []

    num_elements = 10_000
    keys = [i for i in range(num_elements)]

    pq.push(0, 0)
    pq.pop()

    for value in range(num_elements):
        priority = random.randint(1, 10_000)

        start_time = perf_counter()
        pq.push(value, priority)
        push_metrics.append(perf_counter() - start_time)

    while len(pq) > 0:
        start_time = perf_counter()
        pq.pop()
        pop_metrics.append(perf_counter() - start_time)
    pop_metrics.reverse()


    def plot(description, x, metrics):
        fig, ax = plt.subplots(figsize=(6, 3.3))

        ax.plot(x, metrics, label=description)

        ax.set_xlabel('Runs')
        ax.set_ylabel('Time')
        ax.legend()


    x = [i for i in range(num_elements)]
    plot('Push', x, push_metrics)
    plot('Pop', x, pop_metrics)
    plt.tight_layout()
    plt.show()
