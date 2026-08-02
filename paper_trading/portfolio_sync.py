"""
=================================================
Project Phoenix
Portfolio Sync
M54
=================================================
"""

from __future__ import annotations

from paper_trading.paper_context import (
    PaperContext,
)


class PortfolioSync:
    """
    Synchronizes paper trading
    portfolio after each trade.
    """

    # --------------------------------------------------
    # Synchronize Portfolio
    # --------------------------------------------------

    def synchronize(
        self,
        context: PaperContext,
    ) -> PaperContext:
        """
        Update virtual account.
        """

        if context.trade is None:

            return context

        context.balance += (
            context.trade.profit_loss
        )

        context.equity = (
            context.balance
        )

        context.result.statistics = (
            context.statistics
        )

        return context

    # --------------------------------------------------
    # Update Statistics
    # --------------------------------------------------

    def update_statistics(
        self,
        context: PaperContext,
    ) -> PaperContext:
        """
        Synchronize portfolio
        statistics and metadata.
        """

        context.result.balance = (
            context.balance
        )

        context.result.equity = (
            context.equity
        )

        context.result.statistics = (
            context.statistics
        )

        context.set_metadata(
            "balance",
            context.balance,
        )

        context.set_metadata(
            "equity",
            context.equity,
        )

        context.set_metadata(
            "net_profit",
            context.statistics.net_profit,
        )

        context.set_metadata(
            "total_trades",
            context.statistics.total_trades,
        )

        context.set_metadata(
            "win_rate",
            context.statistics.win_rate,
        )

        return context