"""
=================================================
Project Phoenix
Execution Logger
M37
=================================================
"""

from __future__ import annotations

from execution_engine.execution_context import (
    ExecutionContext,
)


class ExecutionLogger:
    """
    Logs execution events.
    """

    def log_start(
        self,
        context: ExecutionContext,
    ) -> None:

        context.metadata["started"] = True

    def log_finish(
        self,
        context: ExecutionContext,
    ) -> None:

        context.metadata["finished"] = True

    def log_failure(
        self,
        context: ExecutionContext,
    ) -> None:

        context.metadata["failed"] = True