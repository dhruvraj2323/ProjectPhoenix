"""
=================================================
Project Phoenix
Scheduler Models
=================================================

Standard scheduler models.
"""

from dataclasses import dataclass


# -------------------------------------------------
# Scheduled Task
# -------------------------------------------------


@dataclass(slots=True)
class ScheduledTask:

    name: str
    interval: int
    enabled: bool
    next_run: str


# -------------------------------------------------
# Scheduler Status
# -------------------------------------------------


@dataclass(slots=True)
class SchedulerStatus:

    running: bool
    tasks_executed: int
    active_tasks: int


# -------------------------------------------------
# Scheduler Result
# -------------------------------------------------


@dataclass(slots=True)
class SchedulerResult:

    approved: bool
    reason: str
    status: SchedulerStatus
    executed_tasks: list[str]