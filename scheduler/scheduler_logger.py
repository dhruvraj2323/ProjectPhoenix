"""
=================================================
Project Phoenix
Scheduler Logger
=================================================

Logs scheduler operations.
"""

from scheduler.scheduler_models import SchedulerResult


class SchedulerLogger:
    """
    Scheduler logging.
    """

    @staticmethod
    def log(result: SchedulerResult):

        print("===== Scheduler =====")

        print(f"Approved        : {result.approved}")
        print(f"Reason          : {result.reason}")
        print()

        print(f"Running         : {result.status.running}")
        print(f"Tasks Executed  : {result.status.tasks_executed}")
        print(f"Active Tasks    : {result.status.active_tasks}")