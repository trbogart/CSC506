# Simple RPN calculator used to test stack implementations (Stack or LinkedList)
import argparse
from typing import Callable

from module4.linked_list import LinkedList
from module4.stack import Stack, IStack


class Calculator:
    def __init__(self, stack: IStack[float]):
        """
        Creates an RPN calculator to test a stack implementation (Stack or LinkedList)
        :param stack: stack to use
        """
        self.stack = stack

    def execute(self) -> None:
        """
        Command-line test program.
        """
        while True:
            print('Stack:')
            if self.stack.is_empty():
                print('- Empty')
            else:
                for i, value in enumerate(iter(self.stack)):
                    pos = len(self.stack) - i
                    if value.is_integer():
                        print(f'- [{pos}] {int(value)}')
                    else:
                        print(f'- [{pos}] {value:.6f}')

            print('Enter number, +, -, *, /, d to drop, s to swap, or q to quit:')
            cmd = input('> ')
            if cmd == 'q':
                break
            elif cmd == '+':
                self.add()
            elif cmd == '-':
                self.subtract()
            elif cmd == '*':
                self.multiply()
            elif cmd == '/':
                self.divide()
            elif cmd == 'd':
                # drop
                if self.stack.is_empty():
                    print('- no values to drop')
                else:
                    self.drop()
            elif cmd == 's':
                # swap
                if len(self.stack) < 2:
                    print('Error: must have at least two values')
                else:
                    self.swap()
            else:
                try:
                    num = float(cmd)
                    self.push_value(num)
                except ValueError:
                    print('Invalid command')

    def push_value(self, num: float):
        self.stack.push(num)

    def drop(self):
        self.stack.pop()

    def divide(self):
        self._binary_op(lambda x, y: x / y)

    def multiply(self):
        self._binary_op(lambda x, y: x * y)

    def subtract(self):
        self._binary_op(lambda x, y: x - y)

    def add(self):
        self._binary_op(lambda x, y: x + y)

    def swap(self):
        value1 = self.stack.pop()
        value2 = self.stack.pop()
        self.push_value(value1)
        self.push_value(value2)

    def _binary_op(self, operation: Callable[[float, float], float]) -> None:
        """
        Perform a binary operation from the two most recent stack values and add the result to the stack.
        :param operation: operation to perform
        :return: new value
        """
        if len(self.stack) < 2:
            print('Error: must have at least two values')
        else:
            value2 = self.stack.pop()
            value1 = self.stack.pop()
            new_value = operation(value1, value2)
            self.push_value(new_value)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='rpn_calculator',
        usage='Simple 4 function RPN calculator used to test stack',
        add_help=True,  # add -h/--help option
    )
    parser.add_argument('-l', '--linked_list', action='store_true',
                        help='Use a linked list implementation (default is to use a Python list implementation)')
    args = parser.parse_args()
    if args.linked_list:
        print('Using linked list')
        stack = LinkedList[float]()
    else:
        print('Using Python list')
        stack = Stack[float]()
    Calculator(stack).execute()
