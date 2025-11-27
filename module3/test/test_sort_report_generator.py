from sort_report_generator import get_median


def test_get_median_1():
    assert get_median([1]) == 1.0


def test_get_median_2():
    assert get_median([2, 1]) == 1.5


def test_get_median_3():
    assert get_median([5, 1, 2]) == 2.0


def test_get_median_4():
    assert get_median([5, 3, 1, 2]) == 2.5


def test_get_median_5():
    assert get_median([4, 6, 3, 1, 2]) == 3.0
