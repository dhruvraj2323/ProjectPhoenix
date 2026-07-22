"""
=================================================
Project Phoenix
Scheduler Engine
=================================================

Master controller for Scheduler.
"""

from scheduler.scheduler_logger import SchedulerLogger
from scheduler.scheduler_models import (
    SchedulerStatus,
    SchedulerResult,
)
from scheduler.scheduler_queue import SchedulerQueue
from scheduler.scheduler_tasks import SchedulerTasks


class SchedulerEngine:
    """
    Master Scheduler Controller.
    """

    def __init__(self):

        self.queue = SchedulerQueue()

    def initialize(self):

        # Register default tasks

        self.queue.register(SchedulerTasks.market_update)
        self.queue.register(SchedulerTasks.signal_generation)
        self.queue.register(SchedulerTasks.risk_evaluation)
        self.queue.register(SchedulerTasks.paper_trading)
        self.queue.register(SchedulerTasks.dashboard_refresh)
        self.queue.register(SchedulerTasks.alert_dispatch)

        results = self.queue.execute()

        status = SchedulerStatus(
            running=True,
            tasks_executed=len(results),
            active_tasks=len(self.queue.tasks),
        )

        result = SchedulerResult(
            approved=True,
            reason="Scheduler initialized successfully.",
            status=status,
            executed_tasks=results,
        )

        SchedulerLogger.log(result)

        return result

    def shutdown(self):
        """
        Shutdown scheduler.
        """

        self.queue.tasks.clear()

        return True