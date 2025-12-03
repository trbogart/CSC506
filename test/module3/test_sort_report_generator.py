from module3.sort_report_generator import get_median


def test_get_median_1():
    assert get_median([1.0]) == 1.0


def test_get_median_2():
    assert get_median([2.0, 1.0]) == 1.5


def test_get_median_3():
    assert get_median([5.0, 1.0, 2.0]) == 2.0


def test_get_median_4():
    assert get_median([5.0, 3.0, 1.0, 2.0]) == 2.5


def test_get_median_5():
    assert get_median([4.0, 6.0, 3.0, 1.0, 2.0]) == 3.0


def test_get_median_6():
    assert get_median([4.0, 6.0, 3.0, 1.0, 7.0, 2.0]) == 3.5
