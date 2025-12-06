import pytest

from module4.deque import Deque
from module4.linked_list import LinkedList
from module4.test_collection import verify_collection
from module4.work_stealing_scheduler import Scheduler, Executor


@pytest.fixture(params=[Deque, LinkedList])
def scheduler(request) -> Scheduler:
    # Build a work stealing scheduler using the given deque implementation
    scheduler = Scheduler()
    for i in range(2):
        Executor(scheduler, request.param())
    return scheduler


def test_work_stealing_scheduler(scheduler):
    executor1 = scheduler.executors[0]
    executor2 = scheduler.executors[1]

    # both executors initially waiting
    verify_executor_waiting(executor1)
    verify_executor_waiting(executor2)

    # schedule job, immediately active
    executor1.schedule_job('1a')
    verify_executor_active(executor1, '1a')
    verify_executor_waiting(executor2)

    # schedule another job, immediately stolen by other executor
    executor1.schedule_job('1b')
    verify_executor_active(executor1, '1a')
    verify_executor_active(executor2, '1b')

    # schedule jobs with no executor available
    executor1.schedule_job('1c')
    verify_executor_active(executor1, '1a', '1c')
    verify_executor_active(executor2, '1b')

    executor2.schedule_job('2a')
    verify_executor_active(executor1, '1a', '1c')
    verify_executor_active(executor2, '1b', '2a')

    executor2.schedule_job('2b')
    verify_executor_active(executor1, '1a', '1c')
    verify_executor_active(executor2, '1b', '2a', '2b')

    executor2.schedule_job('2c')
    verify_executor_active(executor1, '1a', '1c')
    verify_executor_active(executor2, '1b', '2a', '2b', '2c')

    # finish job, pick up scheduled job
    executor2.finish_job()
    verify_executor_active(executor1, '1a', '1c')
    verify_executor_active(executor2, '2a', '2b', '2c')

    executor1.finish_job()
    verify_executor_active(executor1, '1c')
    verify_executor_active(executor2, '2a', '2b', '2c')

    # finish job with no waiting work, steal work from end of other executor's job
    executor1.finish_job()
    verify_executor_active(executor1, '2c')
    verify_executor_active(executor2, '2a', '2b')

    # finish job, no more waiting jobs
    executor2.finish_job()
    verify_executor_active(executor1, '2c')
    verify_executor_active(executor2, '2b')

    # finish remaining jobs with no work on either queue
    executor1.finish_job()
    verify_executor_waiting(executor1)
    verify_executor_active(executor2, '2b')

    executor2.finish_job()
    verify_executor_waiting(executor1)
    verify_executor_waiting(executor2)


def verify_executor_waiting(executor):
    assert executor.is_waiting()
    assert executor.active_job is None
    verify_collection(executor.work_queue)


def verify_executor_active(executor, active_job, *waiting_jobs):
    assert not executor.is_waiting()
    assert executor.active_job == active_job
    verify_collection(executor.work_queue, *waiting_jobs)
