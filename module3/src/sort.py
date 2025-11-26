def bubble_sort(data):
    """Perform a bubble sort on the data."""
    n = len(data)
    # top i elements are sorted
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
    # TODO can optimize by stopping if inner loop does no swaps


def selection_sort(data):
    n = len(data)
    # bottom i elements are sorted
    for i in range(n - 1):
        # find next smallest value to put at i
        for j in range(i + 1, n):
            if data[i] > data[j]:
                data[i], data[j] = data[j], data[i]
    # TODO can optimize by stopping if inner loop does no swaps


def insertion_sort(data):
    # bottom i elements are sorted
    for i in range(1, len(data)):
        # move item backwards until reach beginning of list OR find proper place
        j = i
        while j > 0 and data[j] < data[j - 1]:
            data[j], data[j - 1] = data[j - 1], data[j]
            j -= 1


def merge_sort(data):
    n = len(data)
    if n <= 1:
        return

    # TODO can optimize by doing insertion sort below a certain threshold

    middle = n // 2

    # recursively sort copies of left and right data
    data1 = data[0:middle]
    data2 = data[middle:]
    merge_sort(data1)
    merge_sort(data2)

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
