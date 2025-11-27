from time import perf_counter

import matplotlib.pyplot as plt
import numpy as np

from data_generator import generate_shuffled, generate_partially_sorted, generate_sorted, generate_reverse_sorted
from sort import bubble_sort, selection_sort, insertion_sort, merge_sort

line = '----------------------------------------------------------------------'

sizes = [1_000, 5_000, 10_000, 50_000]
# sizes = [10, 50, 100, 500, 1_000]

data_type_map = {
    'shuffled': generate_shuffled,
    'already sorted': generate_sorted,
    'reverse sorted': generate_reverse_sorted,
    'partially sorted': generate_partially_sorted,
}
sort_type_map = {
    'bubble': bubble_sort,
    'selection': selection_sort,
    'insertion': insertion_sort,
    'merge': merge_sort,
}
num_runs = 3  # take median


def validate_sorted(data):
    for i in range(1, len(data)):
        assert data[i - 1] <= data[i]


if __name__ == '__main__':
    results = []
    best_results = []
    for size in sizes:
        for data_type, data_generator in data_type_map.items():
            print(line)
            print(f'Sorting {size:,} {data_type} elements')
            best_sort_type = None
            best_sort_time_ms = float('inf')
            for sort_type, sort_algorithm in sort_type_map.items():
                print(f'- {sort_type} sort with {size:,} {data_type} elements...', end='\t')
                times = []
                for run in range(num_runs):
                    data = data_generator(size)
                    start_time = perf_counter()
                    sort_algorithm(data)
                    times.append(perf_counter() - start_time)
                    if run == 0:
                        # validate sort algorithm on first run only
                        validate_sorted(data)

                if num_runs > 2:
                    times.sort()
                    drop_times = (num_runs + 1) // 2 - 1
                    times = times[drop_times:-drop_times]
                time_ms = sum(times) * 1000 / len(times)

                print(f'{time_ms:.1f} ms')
                results.append((size, data_type, sort_type, time_ms))

                if time_ms < best_sort_time_ms:
                    best_sort_time_ms = time_ms
                    best_sort_type = sort_type

            print(f'Best sort type for {size:,} {data_type} elements: {best_sort_type}')
            best_results.append((size, data_type, best_sort_type))

    print(line)
    print('All results (csv)')
    print('size,data_type,sort_type,time_ms')
    for size, data_type, sort_type, time_ms in results:
        print(f'{size},{data_type},{sort_type},{time_ms:.1f}')

    print(line)
    print('Best sort type (csv)')
    print('size,data_type,best_sort_type')
    for size, data_type, best_sort_type in best_results:
        print(f'{size},{data_type},{best_sort_type}')

    # graph times for each sort algorithm for each type of data
    # use logarithmic scale to make it easier to compare different algorithms
    log_sizes = np.log10(sizes)
    graph_data = {
        (data_type, sort_type, size): time_ms for size, data_type, sort_type, time_ms in results
    }
    for data_type in data_type_map.keys():
        fig, ax = plt.subplots(figsize=(6, 3.3))
        for sort_type in sort_type_map.keys():
            log_times = np.log10([graph_data[(data_type, sort_type, size)] for size in sizes])

            ax.plot(log_sizes, log_times, label=sort_type)
            ax.set_xlabel('Log₁₀ elements')
            ax.set_ylabel('Log₁₀ time ms')
            ax.legend()

        plt.suptitle(f'{data_type} elements')  # e.g. "sorted elements"
        plt.tight_layout()
        plt.show()
