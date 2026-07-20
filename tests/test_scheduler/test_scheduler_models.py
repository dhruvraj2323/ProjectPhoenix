"""
=================================================
Project Phoenix
Scheduler Models Test
=================================================
"""

from scheduler.scheduler_models import (
    ScheduledTask,
    SchedulerStatus,
    SchedulerResult,
)


def run_test():

    task = ScheduledTask(
        name="Market Update",
        interval=60,
        enabled=True,
        next_run="2026-07-20 10:31:00",
    )

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

    print("===== Scheduler Models =====")

    print(f"Task Name       : {task.name}")
    print(f"Interval        : {task.interval} sec")
    print(f"Tasks Executed  : {status.tasks_executed}")
    print(f"Active Tasks    : {status.active_tasks}")

    assert result.approved

    print()
    print("Scheduler Models Test Passed")


if __name__ == "__main__":

    run_test()