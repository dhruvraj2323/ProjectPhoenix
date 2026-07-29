"""
=================================================
Project Phoenix
Paper Portfolio
M24
=================================================
"""

from __future__ import annotations

from paper_trading.paper_models import (
    PaperPortfolio,
)


class PaperPortfolioManager:
    """
    Maintains virtual paper trading account.
    """

    def __init__(self) -> None:

        self._portfolio = PaperPortfolio()

    def update_floating_profit(
        self,
        profit: float,
    ) -> None:
        """
        Update unrealized PnL.
        """

        self._portfolio.floating_pnl = profit

        self._portfolio.equity = (

            self._portfolio.balance

            + self._portfolio.floating_pnl

        )

    def close_trade(
        self,
        profit: float,
    ) -> None:
        """
        Close virtual trade.
        """

        self._portfolio.realized_pnl += profit

        self._portfolio.balance += profit

        self._portfolio.equity = (

            self._portfolio.balance

            + self._portfolio.floating_pnl

        )

        self._portfolio.total_closed_positions += 1

    def add_position(self) -> None:

        self._portfolio.total_positions += 1

    def remove_position(self) -> None:

        if self._portfolio.total_positions > 0:

            self._portfolio.total_positions -= 1

    def portfolio(
        self,
    ) -> PaperPortfolio:
        """
        Return current virtual portfolio.
        """

        return self._portfolio

    def update_context(
        self,
        context,
    ):
        """
        Synchronize portfolio into PaperContext.
        """

        context.portfolio = self._portfolio

        return context