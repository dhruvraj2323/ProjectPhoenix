"""
=================================================
Project Phoenix
Scheduler Logger Test
=================================================
"""

from scheduler.scheduler_logger import SchedulerLogger
from scheduler.scheduler_models import (
    SchedulerStatus,
    SchedulerResult,
)


def run_test():

    status = SchedulerStatus(
        running=True,
        tasks_executed=15,
        active_tasks=8,
    )

    result = SchedulerResult(
        approved=True,
        reason="Scheduler initialized successfully.",
        status=status,
    )

    SchedulerLogger.log(result)

    assert result.approved

    print()
    print("Scheduler Logger Test Passed")


if __name__ == "__main__":

    run_test()