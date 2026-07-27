"""
=================================================
Project Phoenix
Strategy Logger
M38
=================================================
"""

from __future__ import annotations

import logging

from strategy.strategy_context import (
    StrategyContext,
)


class StrategyLogger:
    """
    Logs Strategy Engine execution.
    """

    def __init__(self) -> None:

        self.logger = logging.getLogger(
            "StrategyEngine",
        )

    def log_start(
        self,
        context: StrategyContext,
    ) -> None:

        self.logger.info(
            "Strategy Engine Started | "
            "Engine=%s Symbol=%s Timeframe=%s",
            context.engine_id,
            context.symbol,
            context.timeframe,
        )

    def log_finish(
        self,
        context: StrategyContext,
    ) -> None:

        self.logger.info(
            "Strategy Engine Finished | "
            "Completed=%s Failed=%s Signals=%d",
            context.completed,
            context.failed,
            len(
                context.strategy_result.signals,
            ),
        )

    def log_failure(
        self,
        context: StrategyContext,
    ) -> None:

        self.logger.error(
            "Strategy Engine Failed | %s",
            context.reason,
        )