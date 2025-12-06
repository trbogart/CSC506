# Simulate a simple message queue that concatenates strings (so ordering of messages matters)
import argparse

from module4.linked_list import LinkedList
from module4.queue import IQueue, Queue


class MessageQueue:
    def __init__(self, queue: IQueue[str]):
        """
        Creates a command-line interface to test a queue implementation (Queue or LinkedList) by appending messages to a string.
        :param queue: queue implementation
        """
        self.queue = queue
        self.value = ''

    def execute(self):
        while True:
            print(f'Current value "{self.value}" with {len(self.queue)} undelivered messages: {self.queue}')
            cmd = input('Enter command (s to send message, r to receive message, q to quit): ')
            if cmd == 'q':
                break
            elif cmd == 's':
                message = input('- Enter message to send: ')
                self.queue.enqueue(message)
            elif cmd == 'r':
                if self.queue.is_empty():
                    print('- No messages to receive')
                else:
                    message = self.queue.dequeue()
                    self.value += message
                    print(f'- Appending {message}')
            else:
                print('- Invalid command')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='message_queue',
        usage='Simple message queue that concatenates message contents',
        add_help=True,  # add -h/--help option
    )
    parser.add_argument('-l', '--linked_list', action='store_true',
                        help='Use a linked list implementation (default is to use a Python list implementation)')
    args = parser.parse_args()
    if args.linked_list:
        print('Using linked list')
        queue = LinkedList[str]()
    else:
        print('Using Python list')
        queue = Queue[str]()
    MessageQueue(queue).execute()
