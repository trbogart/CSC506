from time import perf_counter

from data_generator import generate_shuffled, generate_partially_sorted, generate_sorted, generate_reverse_sorted
from sort import bubble_sort, selection_sort, insertion_sort, merge_sort

sizes = [1000, 5000, 10000, 50000]
data_generators = {
    'shuffled': generate_shuffled,
    'already sorted': generate_sorted,
    'reverse sorted': generate_reverse_sorted,
    'partially sorted': generate_partially_sorted,
}
sort_algorithms = {
    'bubble': bubble_sort,
    'selection': selection_sort,
    'insertion': insertion_sort,
    'merge': merge_sort,
}
num_tests = 5


def validate_sorted(data):
    for i in range(1, len(data)):
        assert data[i - 1] <= data[i]


if __name__ == '__main__':
    results = []
    best_results = []
    for data_type, data_generator in data_generators.items():
        for size in sizes:
            best_sort_type = None
            best_sort_time_ms = float('inf')
            for sort_type, sort_algorithm in sort_algorithms.items():
                description = f'{sort_type} sort with {size:,} {data_type} elements'
                print(f'Testing {description}...', end=' ')
                total_time = 0
                for test in range(num_tests):
                    data = data_generator(size)
                    start_time = perf_counter()
                    sort_algorithm(data)
                    total_time += (perf_counter() - start_time)
                    validate_sorted(data)
                average_time_ms = total_time * 1000 / num_tests
                print(f'{average_time_ms:.1f} ms')
                results.append((data_type, size, sort_type, average_time_ms))

                if average_time_ms < best_sort_time_ms:
                    best_sort_time_ms = average_time_ms
                    best_sort_type = sort_type

            best_results.append((data_type, size, best_sort_type))

    print('--------------------------------------------------')
    print('all results')
    print('data_type,size,sort_type,average_time_ms')
    for data_type, size, sort_type, average_time_ms in results:
        print(f'{data_type},{size},{sort_type},{average_time_ms:.1f}')

    print('--------------------------------------------------')
    print('data_type,size,best_sort_type')
    for (data_type, size, best_sort_type) in best_results:
        print(f'{data_type},{size},{best_sort_type}')
