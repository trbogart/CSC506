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
                self.binary_op(lambda x, y: x + y)
            elif cmd == '-':
                self.binary_op(lambda x, y: x - y)
            elif cmd == '*':
                self.binary_op(lambda x, y: x * y)
            elif cmd == '/':
                self.binary_op(lambda x, y: x / y)
            elif cmd == 'd':
                # drop
                if self.stack.is_empty():
                    print('- no values to drop')
                else:
                    self.stack.pop()
            elif cmd == 's':
                # swap
                if len(self.stack) < 2:
                    print('Error: must have at least two values')
                else:
                    value1 = self.stack.pop()
                    value2 = self.stack.pop()
                    self.stack.push(value1)
                    self.stack.push(value2)
            else:
                try:
                    num = float(cmd)
                    self.stack.push(num)
                except ValueError:
                    print('Invalid command')

    def binary_op(self, operation: Callable[[float, float], float]) -> None:
        """
        Perform a binary operation from the two most recent stack values and add the result to the stack.
        :param operation: operation to perform
        :return: new value
        """
        if len(stack) < 2:
            print('Error: must have at least two values')
        else:
            value2 = stack.pop()
            value1 = stack.pop()
            new_value = operation(value1, value2)
            stack.push(new_value)


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
