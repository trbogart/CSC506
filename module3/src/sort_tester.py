from time import perf_counter

from data_generator import generate_shuffled, generate_partially_sorted, generate_sorted, generate_reverse_sorted
from sort import bubble_sort, selection_sort, insertion_sort, merge_sort

# sizes = [10, 100, 1_000]
sizes = [1_000, 5_000, 10_000, 50_000]

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
    for size in sizes:
        for data_type, data_generator in data_generators.items():
            data_type_csv = data_type.lower().replace(' ', '_')
            print('----------------------------------------------------------------------')
            print(f'Sorting {size:,} {data_type} elements')
            best_sort_type = None
            best_sort_time_ms = float('inf')
            for sort_type, sort_algorithm in sort_algorithms.items():
                print(f'- {sort_type} sort with {size:,} {data_type} elements...', end='\t')
                total_time = 0
                for test in range(num_tests):
                    data = data_generator(size)
                    start_time = perf_counter()
                    sort_algorithm(data)
                    total_time += (perf_counter() - start_time)
                    validate_sorted(data)
                average_time_ms = total_time * 1000 / num_tests
                print(f'{average_time_ms:.1f} ms')
                results.append((size, data_type_csv, sort_type, average_time_ms))

                if average_time_ms < best_sort_time_ms:
                    best_sort_time_ms = average_time_ms
                    best_sort_type = sort_type

            print(f'Best sort type for {size:,} {data_type} elements: {best_sort_type}')
            best_results.append((size, data_type_csv, best_sort_type))

    print('----------------------------------------------------------------------')
    print('All results (csv)')
    print('size,data_type,sort_type,average_time_ms')
    for size, data_type, sort_type, average_time_ms in results:
        print(f'{size},{data_type},{sort_type},{average_time_ms:.1f}')

    print('----------------------------------------------------------------------')
    print('Best sort type (csv)')
    print('size,data_type,best_sort_type')
    for (size, data_type, best_sort_type) in best_results:
        print(f'{size},{data_type},{best_sort_type}')
