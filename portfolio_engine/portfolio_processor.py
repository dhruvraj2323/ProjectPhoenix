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
    Portfolio processing engine.
    """

    def process(
        self,
        context: PortfolioContext,
    ) -> PortfolioContext:
        """
        Process portfolio positions.
        """

        total_profit = 0.0

        winning = 0

        losing = 0

        for position in context.positions:

            total_profit += position.profit_loss

            if position.profit_loss > 0:

                winning += 1

            elif position.profit_loss < 0:

                losing += 1

        context.statistics.total_positions = (
            len(context.positions)
        )

        context.statistics.winning_positions = (
            winning
        )

        context.statistics.losing_positions = (
            losing
        )

        context.statistics.total_profit = max(
            total_profit,
            0.0,
        )

        context.statistics.total_loss = min(
            total_profit,
            0.0,
        )

        context.equity = (
            context.balance + total_profit
        )

        context.free_margin = (
            context.equity - context.margin
        )

        context.completed = True

        return context