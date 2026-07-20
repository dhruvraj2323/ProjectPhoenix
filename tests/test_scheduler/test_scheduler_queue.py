"""
=================================================
Project Phoenix
Scheduler Queue Test
=================================================
"""

from scheduler.scheduler_queue import SchedulerQueue
from scheduler.scheduler_tasks import SchedulerTasks


def run_test():

    queue = SchedulerQueue()

    queue.register(SchedulerTasks.market_update)
    queue.register(SchedulerTasks.signal_generation)
    queue.register(SchedulerTasks.dashboard_refresh)

    results = queue.execute()

    print("===== Scheduler Queue =====")

    for result in results:
        print(result)

    assert len(results) == 3

    print()
    print("Scheduler Queue Test Passed")


if __name__ == "__main__":

    run_test()