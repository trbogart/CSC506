import random


def generate_sorted(n):
    return [i + 1 for i in range(n)]


def generate_unsorted(n):
    data = generate_sorted(n)
    random.shuffle(data)
    return data


def generate_partially_sorted(n, p=.01):
    data = generate_sorted(n)
    for i in range(0, n - 1):
        if random.random() < p:
            data[i], data[i + 1] = data[i + 1], data[i]
    return data


def generate_reverse_sorted(n):
    return [n - i for i in range(n)]
