"""
=================================================
Project Phoenix
Portfolio Processor
M35
=================================================
"""

from __future__ import annotations

from portfolio_engine.portfolio_context import (
    PortfolioContext,
)


class PortfolioProcessor:
    """
    Processes portfolio state and
    updates portfolio statistics.
    """

    def process(
        self,
        context: PortfolioContext,
    ) -> PortfolioContext:

        summary = context.summary

        summary.total_trades = len(
            context.positions
        )

        summary.floating_pnl = sum(

            position.unrealized_pnl

            for position in context.positions

        )

        summary.realized_pnl = sum(

            position.realized_pnl

            for position in context.positions

        )

        summary.equity = (

            summary.balance

            + summary.floating_pnl

        )

        summary.free_margin = (

            summary.equity

            - summary.used_margin

        )

        summary.winning_trades = sum(

            1

            for position in context.positions

            if position.realized_pnl > 0

        )

        summary.losing_trades = sum(

            1

            for position in context.positions

            if position.realized_pnl < 0

        )

        if summary.total_trades > 0:

            summary.win_rate = (

                summary.winning_trades

                / summary.total_trades

            ) * 100.0

        else:

            summary.win_rate = 0.0

        return context