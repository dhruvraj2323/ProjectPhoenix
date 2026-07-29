"""
=================================================
Project Phoenix
Paper Trading Logger
M24
=================================================
"""

from __future__ import annotations

import logging

from paper_trading.paper_context import (
    PaperContext,
)


class PaperLogger:
    """
    Logger for Paper Trading Engine.
    """

    def __init__(self) -> None:

        self.logger = logging.getLogger(
            "PaperTrading",
        )

    def log_start(
        self,
        context: PaperContext,
    ) -> None:

        self.logger.info(

            "Paper trading started | %s",

            context.paper_id,

        )

    def log_summary(
        self,
        context: PaperContext,
    ) -> None:

        portfolio = context.portfolio

        self.logger.info(

            (
                "Paper Summary | "
                "Balance=%.2f | "
                "Equity=%.2f | "
                "OpenPositions=%d"
            ),

            portfolio.balance,

            portfolio.equity,

            portfolio.total_positions,

        )

    def log_finish(
        self,
        context: PaperContext,
    ) -> None:

        self.logger.info(

            "Paper trading completed | %s",

            context.paper_id,

        )

    def log_failure(
        self,
        context: PaperContext,
    ) -> None:

        self.logger.error(

            "Paper trading failed | %s",

            context.reason,

        )