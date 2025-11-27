def bubble_sort(data: list) -> None:
    """
    Perform a bubble insertion sort on the data.
    :param data: The data list to sort in place
    :return: None
    """
    n = len(data)
    # elements above i are sorted
    for i in range(n - 1, -1, -1):
        swapped = False
        for j in range(i):
            if data[j] > data[j + 1]:
                swapped = True
                data[j], data[j + 1] = data[j + 1], data[j]
        if not swapped:
            # optimization to break early if already sorted
            # unlike insertion sort, this only works if completely sorted
            break


def selection_sort(data: list) -> None:
    """
    Perform a selection sort on the data.
    :param data: The data list to sort in place
    :return: None
    """
    n = len(data)
    # bottom i elements are sorted
    for i in range(n - 1):
        # find next smallest value to swap to put at i
        smallest_index = i
        smallest_value = data[i]
        for j in range(i + 1, n):
            current_value = data[j]
            if current_value < smallest_value:
                smallest_index = j
                smallest_value = current_value
        if smallest_index != i:
            data[i], data[smallest_index] = data[smallest_index], data[i]


def insertion_sort(data: list) -> None:
    """
    Perform an insertion sort on the data.
    :param data: The data list to sort in place
    :return: None
    """
    # bottom i elements are sorted
    for i in range(1, len(data)):
        # move item backwards until reach beginning of list OR find proper place
        j = i
        while j > 0 and data[j] < data[j - 1]:
            data[j], data[j - 1] = data[j - 1], data[j]
            j -= 1


def merge_sort(data: list, merge_threshold: int = 10) -> None:
    """
    Perform a merge sort on the data.
    :param data: The data list to sort in place
    :param merge_threshold: Minimum size to do merge, do insertion sort below this size
    :return: None
    """
    n = len(data)
    if n <= 1:
        return

    # use insertion sort at or below the merge size threshold
    if n <= merge_threshold:
        insertion_sort(data)
        return

    middle = n // 2

    # recursively sort copies of left and right data
    data1 = data[0:middle]
    data2 = data[middle:]
    merge_sort(data1, merge_threshold)
    merge_sort(data2, merge_threshold)

    # merge left and right data
    n1 = len(data1)
    n2 = len(data2)
    i1 = 0
    i2 = 0

    for i in range(n):
        if i1 < n1:
            if i2 < n2:
                # both arrays have elements remaining, take smaller
                if data1[i1] <= data2[i2]:
                    data[i] = data1[i1]
                    i1 += 1
                else:
                    data[i] = data2[i2]
                    i2 += 1
            else:
                # only data1 has elements remaining
                data[i] = data1[i1]
                i1 += 1
        else:
            # only data2 has elements remaining
            data[i] = data2[i2]
            i2 += 1


def merge_sort_pure(data: list) -> None:
    """
    Perform a pure merge sort on the data without using insertion sort for smaller sublists.
    :param data: The data list to sort in place
    :return: None
    """
    merge_sort(data, merge_threshold=0)
