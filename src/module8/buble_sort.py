# Sorting implementations
from random import shuffle

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

def bubble_sort(data):
    """
    Perform a bubble insertion sort on the data.
    :param data: The data list to be sorted
    :return: None
    """
    n = len(data)
    # elements above i are sorted
    for i in range(n - 1, -1, -1):
        any_swapped = False
        for j in range(i):
            elements_swapped = data[j] > data[j + 1]
            if elements_swapped:
                any_swapped = True
                data[j], data[j + 1] = data[j + 1], data[j]
            yield j, data[j], j + 1, data[j+1], elements_swapped, i+1
        if not any_swapped:
            break

def bubble_sort_demo(length, filename) -> None:
    print(f'Saving bubblesort demo for length {length} to {filename}')
    data = [i+1 for i in range(length)]
    shuffle(data)

    # I used ChatGPT for help with visualization
    fig, ax = plt.subplots()
    ax.set_title(f'Bubble Sort')
    bars = ax.bar(range(len(data)), data, color = 'blue')

    steps = list(bubble_sort(data))

    def update(frame):
        idx1, data1, idx2, data2, swapped, min_sorted = steps[frame]
        for idx, bar in enumerate(bars):
            bar = bars[idx]
            if idx == idx1:
                bar.set_height(data1)
                bar.set_color('red' if swapped else 'orange')
            elif idx == idx2:
                bar.set_height(data2)
                bar.set_color('red' if swapped else 'orange')
            else:
                bar.set_color('blue')

            if idx >= min_sorted:
                bar.set_color('green')
                break
        return bars

    ani = FuncAnimation(fig, update, frames=len(steps), interval=100, blit=False)

    # PilloWriter with no loop, from
    # https://stackoverflow.com/questions/64529921/the-saved-animated-plot-keeps-looping-although-matplotlib-funcanimation-repe
    class PillowWriterNG(PillowWriter):
        def finish(self):
            self._frames[0].save(
                self.outfile, save_all=True, append_images=self._frames[1:],
                duration=int(1000 / self.fps), loop=None)

    ani.save(filename, writer=PillowWriterNG(fps=16))
    plt.close(fig)

if __name__ == "__main__":
    bubble_sort_demo(16, 'bubble_sort.gif')