from random import seed, shuffle

from module8.bubble_sort import bubble_sort, Step


def test_bubble_sort():
    orig_data = [i + 1 for i in range(100)]
    seed(137)
    data = orig_data[:]
    shuffle(data)
    bubble_sort(data)

    assert data == orig_data


def test_bubble_sort_steps():
    data = [11, 14, 13, 10, 12]

    steps = []
    bubble_sort(data, steps.append)
    assert len(steps) == 10

    assert data == [10, 11, 12, 13, 14]

    # 1st outer loop: move largest element into place
    validate_step(steps[0], idx1=0, idx2=1, data1=11, data2=14, swapped=False,
                  min_sorted=5)  # do not swap 11 and 14: [11, 14, 13, 10, 12]
    validate_step(steps[1], idx1=1, idx2=2, data1=13, data2=14, swapped=True,
                  min_sorted=5)  # swap 13 and 14: [11, 13, 14, 10, 12]
    validate_step(steps[2], idx1=2, idx2=3, data1=10, data2=14, swapped=True,
                  min_sorted=5)  # swap 10 and 14: [11, 13, 10, 14, 12]
    validate_step(steps[3], idx1=3, idx2=4, data1=12, data2=14, swapped=True,
                  min_sorted=5)  # swap 12 and 14: [11, 13, 10, 12, 14]
    # 2nd outer loop: move 2nd largest element into place
    validate_step(steps[4], idx1=0, idx2=1, data1=11, data2=13, swapped=False, min_sorted=4)  # do not swap 11 and 13
    validate_step(steps[5], idx1=1, idx2=2, data1=10, data2=13, swapped=True,
                  min_sorted=4)  # swap 10 and 13: [11, 10, 13, 12, 14]
    validate_step(steps[6], idx1=2, idx2=3, data1=12, data2=13, swapped=True,
                  min_sorted=4)  # swap 12 and 13: [11, 10, 12, 13, 14]
    # 3rd outer loop: move 3rd largest element into place
    validate_step(steps[7], idx1=0, idx2=1, data1=10, data2=11, swapped=True,
                  min_sorted=3)  # swap 10 and 11: [10, 11, 12, 13, 14]
    validate_step(steps[8], idx1=1, idx2=2, data1=11, data2=12, swapped=False, min_sorted=3)  # do not swap 11 and 12
    # 4th outer loop: move 4th largest element into place
    validate_step(steps[9], idx1=0, idx2=1, data1=10, data2=11, swapped=False, min_sorted=2)  # do not swap 10 and 11


def test_bubble_sort_steps_abort_early():
    data = [11, 10, 12, 14, 13]

    steps = []
    bubble_sort(data, steps.append)
    assert len(steps) == 7

    assert data == [10, 11, 12, 13, 14]

    # 1st outer loop: move largest element into place
    validate_step(steps[0], idx1=0, idx2=1, data1=10, data2=11, swapped=True,
                  min_sorted=5)  # swap 10 and 11: [10, 11, 12, 14, 13]
    validate_step(steps[1], idx1=1, idx2=2, data1=11, data2=12, swapped=False, min_sorted=5)  # do not swap 11 and 12
    validate_step(steps[2], idx1=2, idx2=3, data1=12, data2=14, swapped=False, min_sorted=5)  # do not swap 12 and 14
    validate_step(steps[3], idx1=3, idx2=4, data1=13, data2=14, swapped=True,
                  min_sorted=5)  # swap 10 and 11: [10, 11, 12, 13, 14]

    # 2nd outer loop: move 2nd largest element into place
    validate_step(steps[4], idx1=0, idx2=1, data1=10, data2=11, swapped=False, min_sorted=4)  # do not swap 10 and 11
    validate_step(steps[5], idx1=1, idx2=2, data1=11, data2=12, swapped=False, min_sorted=4)  # do not swap 11 and 12
    validate_step(steps[6], idx1=2, idx2=3, data1=12, data2=13, swapped=False, min_sorted=4)  # do not swap 12 and 13

    # abort after 2nd outer loop: no more swaps


def validate_step(step, idx1, data1, idx2, data2, swapped, min_sorted):
    assert step == Step(idx1=idx1, data1=data1, idx2=idx2, data2=data2, swapped=swapped, min_sorted=min_sorted)
