"""
=================================================
Project Phoenix
Execution Logger
M37
=================================================
"""

from __future__ import annotations

import logging

from execution_engine.execution_context import (
    ExecutionContext,
)


class ExecutionLogger:
    """
    Logger for Execution Engine.
    """

    def __init__(self) -> None:

        self.logger = logging.getLogger(
            "ExecutionEngine"
        )

    def log_start(
        self,
        context: ExecutionContext,
    ) -> None:

        self.logger.info(
            "Execution started | %s | %s",
            context.execution_id,
            context.symbol,
        )

    def log_order(
        self,
        context: ExecutionContext,
    ) -> None:

        if context.order is None:
            return

        self.logger.info(

            "Order Created | %s | %s | %.2f",

            context.order.symbol,

            context.order.side,

            context.order.entry_price,

        )

    def log_finish(
        self,
        context: ExecutionContext,
    ) -> None:

        self.logger.info(

            "Execution finished | %s",

            context.execution_result.status.value,

        )

    def log_failure(
        self,
        context: ExecutionContext,
    ) -> None:

        self.logger.error(

            "Execution failed | %s",

            context.reason,

        )