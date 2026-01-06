from random import seed, shuffle

from module8.quickselect import quickselect


def test_quickselect():
    data = [i + 1 for i in range(100)]
    seed(137)
    shuffle(data)

    for k in range(len(data)):
        assert quickselect(data, k) == k + 1
