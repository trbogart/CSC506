import random


from module5.priority_queue import PriorityQueue

class PriorityQueueDemo:
    def __init__(self):
        self.pq = PriorityQueue()


    def push(self, num_elements: int = 1):
        for value in range(num_elements):
            priority = random.randint(101, 200)
            self.pq.push(value, priority)
            print(f'Inserted {value} with priority {priority} into priority queue, size {len(self.pq)}')

    def pop(self):
        while len(self.pq) > 0:
            value, priority = self.pq.peek()
            print(f'Peek   {value} with priority {priority} from priority queue, size {len(self.pq)}')
            value, priority = self.pq.pop()
            print(f'Popped {value} with priority {priority} from priority queue, size {len(self.pq)}')

if __name__ == '__main__':
    pq_demo = PriorityQueueDemo()
    pq_demo.push(10)
    pq_demo.pop()

