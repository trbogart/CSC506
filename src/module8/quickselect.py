def quickselect(data, k):
    """
    Uses quickselect algorithm to find the kth smallest element in data (0-based).
    :param data: data to search
    :param k: element to find (0 for smallest, 1 for next smallest, etc.)
    :return: element
    """
    return _quickselect(data, 0, len(data) - 1, k)


def _quickselect(data, start_index, end_index, k):
    """
    Quickselect
    :param data: data to search
    :param start_index: start index, inclusive
    :param end_index: end index, inclusive
    :param k: element to find (0 for smallest, 1 for next smallest, etc.)
    :return:
    """
    # Adapted from CS506: Design and Analysis of Algorithms, chapter 8.7

    if start_index >= end_index:
        return data[start_index]

    low_last_index = _partition(data, start_index, end_index)
    if k <= low_last_index:
        # continue in left partition
        return _quickselect(data, start_index, low_last_index, k)
    # continue in right partition
    return _quickselect(data, low_last_index + 1, end_index, k)


def _partition(data, start_index, end_index):
    """
    Partition an array.
    :param data: data to partition
    :param start_index: start index, inclusive
    :param end_index: end index, inclusive
    :return: last index in the left segment.
    """

    # Adapted from CS506: Design and Analysis of Algorithms, chapter 3.9

    # Select the middle value as the pivot.
    midpoint = start_index + (end_index - start_index) // 2
    pivot = data[midpoint]

    # "low" and "high" start at the ends of the list segment and move towards each other.
    low = start_index
    high = end_index

    done = False
    while not done:
        # Increment low while numbers[low] < pivot
        while data[low] < pivot:
            low = low + 1

        # Decrement high while pivot < numbers[high]
        while pivot < data[high]:
            high = high - 1

        # If low and high have crossed each other, the loop is done.
        # If not, the elements are swapped, low is incremented and high is decremented.
        if low >= high:
            done = True
        else:
            temp = data[low]
            data[low] = data[high]
            data[high] = temp
            low = low + 1
            high = high - 1

    # return last index in the left segment.
    return high
