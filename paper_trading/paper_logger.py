"""
=================================================
Project Phoenix
Paper Trading Logger
M54
=================================================
"""

from __future__ import annotations

import logging

from paper_trading.paper_context import (
    PaperContext,
)


class PaperLogger:
    """
    Logging utility for the
    Paper Trading Engine.
    """

    def __init__(
        self,
    ) -> None:

        self.logger = logging.getLogger(
            "PaperTradingEngine",
        )

    # --------------------------------------------------
    # Log Start
    # --------------------------------------------------

    def log_start(
        self,
        context: PaperContext,
    ) -> None:
        """
        Log engine start.
        """

        self.logger.info(

            "Paper Trading started | "
            "Paper ID=%s | "
            "Symbol=%s | "
            "Timeframe=%s",

            context.paper_id,

            context.symbol,

            context.timeframe,

        )

    # --------------------------------------------------
    # Log Failure
    # --------------------------------------------------

    def log_failure(
        self,
        context: PaperContext,
    ) -> None:
        """
        Log failed execution.
        """

        self.logger.error(

            "Paper Trading failed | "
            "Paper ID=%s | "
            "Reason=%s",

            context.paper_id,

            context.reason,

        )

    # --------------------------------------------------
    # Log Finish
    # --------------------------------------------------

    def log_finish(
        self,
        context: PaperContext,
    ) -> None:
        """
        Log successful completion.
        """

        self.logger.info(

            "Paper Trading completed | "
            "Paper ID=%s | "
            "Balance=%.2f | "
            "Equity=%.2f | "
            "Trades=%d | "
            "Net Profit=%.2f",

            context.paper_id,

            context.balance,

            context.equity,

            context.statistics.total_trades,

            context.statistics.net_profit,

        )