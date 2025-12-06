import pytest

from module4.linked_list import LinkedList
from module4.rpn_calculator import Calculator
from module4.stack import Stack
from module4.test_collection import verify_collection


@pytest.fixture(params=[Stack, LinkedList])
def calculator(request) -> Calculator:
    # Instantiate the stack implementation and use it build an RPN calculator
    return Calculator(request.param())


def test_calculator(calculator):
    verify_collection(calculator.stack)

    calculator.push_value(3)
    verify_collection(calculator.stack, 3)

    calculator.push_value(2)
    verify_collection(calculator.stack, 3, 2)

    calculator.push_value(1)
    verify_collection(calculator.stack, 3, 2, 1)

    calculator.add()
    verify_collection(calculator.stack, 3, 3)

    calculator.multiply()
    verify_collection(calculator.stack, 9)

    calculator.push_value(1)
    verify_collection(calculator.stack, 9, 1)

    calculator.subtract()
    verify_collection(calculator.stack, 8)

    calculator.push_value(2)
    verify_collection(calculator.stack, 8, 2)

    calculator.divide()
    verify_collection(calculator.stack, 4.0)

    calculator.push_value(1)
    verify_collection(calculator.stack, 4.0, 1)

    calculator.swap()
    verify_collection(calculator.stack, 1, 4.0)

    calculator.drop()
    verify_collection(calculator.stack, 1)

    calculator.drop()
    verify_collection(calculator.stack)
