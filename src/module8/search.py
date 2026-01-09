def linear_search(a, value):
    """
    Performs a linear search for an element in a list.
    :param a: list (or other iterable) to search
    :param value: the value to search for
    :return: the index of the given element in the list
    :raises ValueError: If element not found
    """
    for i, element in enumerate(a):
        if element == value:
            return i
    raise ValueError("Element not found")


def binary_search(a, value):
    """
    Performs a binary search for an element in a sorted list.
    :param a:  sorted list that supports  random-access retrieval
    :param value: the value to search for
    :return: the index of the given element in the list
    :raises ValueError: If element not found
    """
    low = 0
    high = len(a) - 1
    while low <= high:
        mid = (low + high) // 2
        if value == a[mid]:
            return mid
        elif value < a[mid]:
            high = mid - 1
        else:
            low = mid + 1
    raise ValueError("Element not found")
