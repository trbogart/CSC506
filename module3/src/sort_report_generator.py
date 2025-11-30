from time import perf_counter

import matplotlib.pyplot as plt
import numpy as np

import data_generator as dg
import sort

# sizes to test
sizes = [1_000, 5_000, 10_000, 50_000]

data_type_map = {
    # data type name to data generator function
    'shuffled': dg.generate_shuffled,
    'reverse sorted': dg.generate_reverse_sorted,
    'partially sorted': dg.generate_partially_sorted,
    'already sorted': dg.generate_sorted,
}
sort_type_map = {
    # sort type name to sort function
    'bubble': sort.bubble_sort,
    'selection': sort.selection_sort,
    'insertion': sort.insertion_sort,
    'merge': sort.merge_sort,
    # 'default': lambda x: x.sort(),
}
# maximum number of runs
max_num_runs = 10
# stop adding runs if total time in seconds is more than this
max_total_seconds_for_next_run = 10
# horizontal separator
line = '-' * 80


def validate_sorted(a: list[int]) -> None:
    """
    Validates if the data is sorted.
    :param a: data to validate
    :return: None
    """
    for i in range(1, len(a)):
        assert a[i - 1] <= a[i]


def get_median(times: list[float]) -> float:
    """
    Returns the mean of the middle third of the data.
    :param times: array of values
    :return: the mean of the middle third of the data
    """
    num_runs = len(times)
    if num_runs > 2:
        times.sort()
        drop_times = num_runs // 3
        times = times[drop_times:-drop_times]
    return sum(times) / len(times)


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
                label = f'- {sort_type} sort: '
                print(f'{label:<18}', end='')
                times_s: list[float] = []
                for run in range(max_num_runs):
                    data = data_generator(size)
                    start_time = perf_counter()
                    sort_algorithm(data)
                    times_s.append(perf_counter() - start_time)
                    if run == 0:
                        # validate sort algorithm on first run only
                        validate_sorted(data)
                    if sum(times_s) > max_total_seconds_for_next_run:
                        # skip multiple runs for slower runs
                        # (multiple runs are more useful and less painful for shorter runs anyway)
                        break

                time_s = get_median(times_s)

                print(f'{time_s:.6f} s')
                results.append((size, data_type, sort_type, time_s))

                if time_s < best_sort_time_ms:
                    best_sort_time_ms = time_s
                    best_sort_type = sort_type

            print(f'Best sort type for {size:,} {data_type} elements: {best_sort_type}')
            best_results.append((size, data_type, best_sort_type))

    print(line)
    print('All results (csv)')
    print('size,data_type,sort_type,time_sec')
    for size, data_type, sort_type, time_s in results:
        print(f'{size},{data_type},{sort_type},{time_s:.6f}')

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
