class PriorityQueue[T]:
    """
    Priority queue implemented using a min heap.
    """
    class Value:
        def __init__(self, priority: int, value: T):
            self.priority = priority
            self.value = value

    def __init__(self):
        self.min_heap = []

    def __len__(self) -> int:
        return len(self.min_heap)

    def push(self, priority: int, value: T) -> None:
        self.min_heap.append(self.Value(priority, value))
        self._move_up(len(self.min_heap) - 1)

    def pop(self) -> T:
        if len(self.min_heap) == 0:
            raise IndexError('Priority queue is empty')
        if len(self.min_heap) == 1:
            return self.min_heap.pop().value

        # swap first and last entries
        last_index = len(self.min_heap) - 1
        self.min_heap[0], self.min_heap[last_index] = self.min_heap[last_index], self.min_heap[0]

        # pop last element and move head to correct location
        value = self.min_heap.pop().value
        self._move_down(0)
        return value

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
