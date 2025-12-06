# Simulates a work-stealing scheduler using a deque (see https://en.wikipedia.org/wiki/Work_stealing).
# Each executor has its own work queue, and will work through scheduled jobs.
# If an executor reaches the end of its queue, it steals work from the end of another executor's queue.
# Note that this implementation is not thread safe, and only meant to simulate a scheduler.
import argparse

from module4.deque import IDeque, Deque
from module4.linked_list import LinkedList


class Scheduler:
    """
    Creates a work-stealing scheduler.
    """

    def __init__(self):
        self.executors = list[Executor]()

    def start_on_waiting_executor(self, job: str) -> bool:
        """
        Start job on waiting executor, if any
        :param job: job to start
        :return: true if the job was started
        """
        for executor in self.executors:
            if executor.is_waiting():
                executor.start_job(job, 'scheduled on another executor while this executor was waiting')
                return True
        return False

    def steal_work(self) -> tuple[int, str | None]:
        """
        Steal work from end of an active executor's queue (if any)
        :return: tuple containing executor index and job that was stolen, or -1 and None if no work was stolen
        """
        # steal work from end of executor's queue (if any)
        for executor in self.executors:
            if not executor.work_queue.is_empty():
                # steal work from executor (this implies that the executor is currently working on something else)
                assert not executor.is_waiting()
                return executor.index, executor.work_queue.remove_rear()
        return -1, None

    def get_executor(self, executor_str: str):
        executor_num = int(executor_str)
        try:
            return self.executors[executor_num - 1]
        except IndexError:
            raise ValueError(f'Invalid executor #{executor_str}')

    def execute(self):
        while True:
            print('------------------------------------------')
            for executor in self.executors:
                executor.print()
            cmd = input(
                'Enter command (s# to schedule job on executor, f# to finish job on executor, or q to quit): ').lower()
            if cmd == 'q':
                break
            elif cmd.startswith('s'):
                try:
                    executor = self.get_executor(cmd[1:])
                    job = input('Enter job: ')
                    executor.schedule_job(job)
                except ValueError:
                    print(f'Invalid executor #{cmd[1:]})')
            elif cmd.startswith('f'):
                try:
                    executor = self.get_executor(cmd[1:])
                    if executor.is_waiting():
                        print(f'Executor #{cmd[1:]} is not active')
                    else:
                        executor.finish_job()
                except ValueError:
                    print(f'Invalid executor #{cmd[1:]})')
            else:
                print('Invalid command')


class Executor:
    def __init__(self, scheduler: Scheduler, work_queue: IDeque[str]):
        self.active_job: str | None = None
        self.scheduler = scheduler
        self.scheduler.executors.append(self)
        self.index = len(scheduler.executors)
        self.work_queue = work_queue

    def print(self):
        print(f'Executor #{self.index}:')
        print(f'  Active job: {self.active_job}')
        print(f'  Work queue: {self.work_queue}')

    def is_waiting(self) -> bool:
        """
        Returns true if the executor does not have an active job.
        """
        return self.active_job is None

    def schedule_job(self, job: str) -> bool:
        """
        Schedule the given job.
        :param job: job
        :return: true if the work has started, false if it has been scheduled to start later
        """
        print(f'Schedule job {job} on executor #{self.index}')
        if self.active_job is None:
            # start job immediately if not already working on another job
            self.start_job(job, 'started immediately')
            return True
        elif self.scheduler.start_on_waiting_executor(job):
            # started by an idle executor
            return True
        else:
            # no available executor, so schedule on this executor's work queue
            self.work_queue.add_rear(job)
            return False

    def start_job(self, job: str, description: str) -> None:
        assert self.active_job is None
        print(f'Executor {self.index} starting job {job}: {description}')
        self.active_job = job

    def finish_job(self):
        assert self.active_job is not None
        print(f'Executor {self.index} finished job {self.active_job}')
        self.active_job = None
        if self.work_queue.is_empty():
            executor_index, stolen_job = self.scheduler.steal_work()
            if executor_index >= 0:
                self.start_job(stolen_job, f"stolen from end of executor #{executor_index}'s work queue")
            else:
                print(f'Executor {self.index} waiting for work')
        else:
            self.start_job(self.work_queue.remove_front(), 'next item in work queue')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='work_stealing',
        usage='Simple message deque that concatenates message contents',
        add_help=True,  # add -h/--help option
    )
    parser.add_argument('-n', '--num', type=int, default=2, help='Number of executors to use')
    parser.add_argument('-l', '--linked_list', action='store_true',
                        help='Use a linked list implementation (default is to use a Python list implementation)')
    args = parser.parse_args()

    scheduler = Scheduler()

    if args.linked_list:
        print(f'Using linked list with {args.num} executors')
    else:
        print(f'Using Python list with {args.num} executors')

    for i in range(args.num):
        if args.linked_list:
            deque = LinkedList[str]()
        else:
            deque = Deque[str]()

        executor = Executor(scheduler, deque)
    scheduler.execute()
