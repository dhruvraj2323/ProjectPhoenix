"""
=================================================
Project Phoenix
Paper Portfolio
=================================================

Maintains virtual portfolio.
"""

from paper_trading.paper_models import PaperPortfolio


class PaperPortfolioManager:
    """
    Maintains paper trading portfolio.
    """

    def __init__(self):

        self.balance = 10000.0
        self.closed_profit = 0.0
        self.floating_profit = 0.0

    def update_floating_profit(self, profit: float):

        self.floating_profit = profit

    def close_trade(self, profit: float):

        self.closed_profit += profit
        self.balance += profit

    def portfolio(self):

        return PaperPortfolio(
            balance=self.balance,
            equity=self.balance + self.floating_profit,
            floating_profit=self.floating_profit,
            closed_profit=self.closed_profit,
        )