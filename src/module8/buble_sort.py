from dataclasses import dataclass
from random import shuffle

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter


@dataclass
class Step:
    idx1: int
    idx2: int
    data1: int
    data2: int
    swapped: bool
    min_sorted: int


def bubble_sort(data, step_callback=None):
    """
    Perform a bubble sort on the data.
    :param data: The data list to be sorted
    :param step_callback: Optional callback that takes a Step argument
    :return: None
    """
    n = len(data)
    # elements > i are sorted
    for i in range(n - 1, -1, -1):
        any_swapped = False
        for j in range(i):
            swapped = data[j] > data[j + 1]
            if swapped:
                any_swapped = True
                data[j], data[j + 1] = data[j + 1], data[j]
            if step_callback is not None:
                step_callback(
                    Step(idx1=j, data1=data[j], idx2=j + 1, data2=data[j + 1], swapped=swapped, min_sorted=i + 1))
        if not any_swapped:
            break


def bubble_sort_demo(length, filename) -> None:
    print(f'Saving bubblesort demo for length {length} to {filename}')
    data = [i + 1 for i in range(length)]
    shuffle(data)

    # I used ChatGPT and StockOverflow for help with visualization, but ended up changing a lot
    fig, ax = plt.subplots()
    ax.set_title(f'Bubble Sort')
    bars = ax.bar(range(len(data)), data, color='blue')

    steps = []
    bubble_sort(data, steps.append)

    refresh = set()

    def update(frame):
        if frame > 0:
            step = steps[frame - 1]
            updated = (step.idx1, step.idx2)
            refresh.update(updated)
            update_color = 'red' if step.swapped else 'yellow'
            for idx in refresh:
                bar = bars[idx]
                if idx == step.idx1:
                    bar.set_height(step.data1)
                    bar.set_color(update_color)
                elif idx == step.idx2:
                    bar.set_height(step.data2)
                    bar.set_color(update_color)
                else:
                    bar.set_color('blue')
            if step.min_sorted < length:
                bars[step.min_sorted].set_color('green')
            refresh.clear()
            refresh.update(updated)
        return bars

    # add an extra frame for initial data
    frames = len(steps) + 1
    ani = FuncAnimation(fig, update, frames=frames, interval=100, blit=False)

    # PillowWriter with no loop, from
    # https://stackoverflow.com/questions/64529921/the-saved-animated-plot-keeps-looping-although-matplotlib-funcanimation-repe

    # Source - https://stackoverflow.com/a
    # Posted by Shaped Sundew, modified by community. See post 'Timeline' for change history
    # Retrieved 2026-01-05, License - CC BY-SA 4.0

    class PillowWriterNG(PillowWriter):
        def finish(self):
            self._frames[0].save(
                self.outfile, save_all=True, append_images=self._frames[1:],
                duration=int(1000 / self.fps), loop=None)

    ani.save(filename, writer=PillowWriterNG(fps=20))
    plt.close(fig)


if __name__ == "__main__":
    bubble_sort_demo(20, 'bubble_sort.gif')
