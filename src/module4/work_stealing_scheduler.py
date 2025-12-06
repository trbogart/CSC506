# Simulates a work-stealing scheduler using a deque (see https://en.wikipedia.org/wiki/Work_stealing).
# Each executor has its own work queue, and will work through scheduled jobs.
# If an executor reaches the end of its queue, it steals work from the end of another executor's queue.
# Note that this implementation is not thread safe, and only meant to simulate a scheduler.
# Also, the job is just a string rather than an executable.
import argparse

from module4.deque import IDeque, Deque
from module4.linked_list import LinkedList


class Scheduler:
    """
    Creates a simulator for work-stealing scheduler.
    """

    def __init__(self):
        self.executors = list[Executor]()

    def _start_on_waiting_executor(self, job: str) -> bool:
        """
        Internal method to start job on an idle executor, if any
        :param job: job to start
        :return: true if the job was started
        """
        for executor in self.executors:
            if executor.is_idle():
                executor._start_job(job, 'scheduled on another executor while this executor was waiting')
                return True
        return False

    def _steal_work(self) -> tuple[int, str | None]:
        """
        Internal method to steal work from the end of an active executor's queue (if any)
        :return: tuple containing executor index and job that was stolen, or -1 and None if no work was stolen
        """
        # steal work from end of executor's queue (if any)
        for executor in self.executors:
            if not executor.work_queue.is_empty():
                # steal work from executor (this implies that the executor is currently working on something else)
                assert not executor.is_idle()
                return executor.index, executor.work_queue.remove_rear()
        return -1, None

    def get_executor(self, executor_str: str):
        """
        Returns the executor with the index corresponding to the given string.
        :param executor_str: executor string (1 based)
        :return: The executor with the index corresponding to the given string.
        :raise ValueError: invalid executor string
        """
        executor_num = int(executor_str)
        try:
            return self.executors[executor_num - 1]
        except IndexError:
            raise ValueError(f'Invalid executor #{executor_str}')

    def execute(self) -> None:
        """
        Command-line test program.
        """
        while True:
            print('------------------------------------------')
            for executor in self.executors:
                print(f'Executor #{executor.index}:')
                print(f'  Active job: {executor.active_job}')
                print(f'  Work queue: {executor.work_queue}')
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
                    if executor.is_idle():
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

    def is_idle(self) -> bool:
        """
        Returns true if the executor does not have an active job.
        """
        return self.active_job is None

    def schedule_job(self, job: str) -> bool:
        """
        Schedule the given job.
        Will start immediately on this executor if idle.
        Otherwise, will start immediately on another idle executor, if any.
        Will be added to this executor's work queue if there are no idle executors.
        :param job: job to perform
        :return: true if the work has started, false if it has been scheduled to start later
        """
        print(f'Schedule job {job} on executor #{self.index}')
        if self.active_job is None:
            # start job immediately if not already working on another job
            self._start_job(job, 'started immediately')
            return True
        elif self.scheduler._start_on_waiting_executor(job):
            # started by an idle executor
            return True
        else:
            # no available executor, so schedule on this executor's work queue
            self.work_queue.add_rear(job)
            return False

    def finish_job(self) -> None:
        """
        Finish a job. Will pick up job from work queue.
        Otherwise, will pick up job from end of another executor's queue.
        Finally, will go idle if no pending work is available on any executor's queue.
        :return:
        """
        assert self.active_job is not None
        print(f'Executor {self.index} finished job {self.active_job}')
        self.active_job = None
        if self.work_queue.is_empty():
            executor_index, stolen_job = self.scheduler._steal_work()
            if executor_index >= 0:
                self._start_job(stolen_job, f"stolen from end of executor #{executor_index}'s work queue")
            else:
                print(f'Executor {self.index} waiting for work')
        else:
            self._start_job(self.work_queue.remove_front(), 'next item in work queue')

    def _start_job(self, job: str, description: str) -> None:
        """
        Internal method to start a new job.
        :param job: job to start
        :param description: description for command-line program
        """
        assert self.active_job is None
        print(f'Executor {self.index} starting job {job}: {description}')
        self.active_job = job


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='work_stealing_scheduler',
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
