"""
=================================================
Project Phoenix
Portfolio Logger
M35
=================================================
"""

from __future__ import annotations

import logging

from portfolio_engine.portfolio_context import (
    PortfolioContext,
)


class PortfolioLogger:
    """
    Logger for Portfolio Engine.
    """

    def __init__(self) -> None:

        self.logger = logging.getLogger(
            "PortfolioEngine",
        )

    def log_start(
        self,
        context: PortfolioContext,
    ) -> None:

        self.logger.info(

            "Portfolio processing started | %s",

            context.portfolio_id,

        )

    def log_summary(
        self,
        context: PortfolioContext,
    ) -> None:

        summary = context.summary

        self.logger.info(

            (
                "Portfolio Summary | "
                "Trades=%d | "
                "Balance=%.2f | "
                "Equity=%.2f | "
                "FloatingPnL=%.2f | "
                "RealizedPnL=%.2f | "
                "WinRate=%.2f%%"
            ),

            summary.total_trades,

            summary.balance,

            summary.equity,

            summary.floating_pnl,

            summary.realized_pnl,

            summary.win_rate,

        )

    def log_finish(
        self,
        context: PortfolioContext,
    ) -> None:

        self.logger.info(

            "Portfolio processing completed | %s",

            context.portfolio_id,

        )

    def log_failure(
        self,
        context: PortfolioContext,
    ) -> None:

        self.logger.error(

            "Portfolio processing failed | %s",

            context.reason,

        )