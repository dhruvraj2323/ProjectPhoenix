"""
=================================================
Project Phoenix
Live Trading Engine
=================================================

Master controller of Live Trading Layer.
"""

from live_trading.live_logger import LiveLogger
from live_trading.live_models import (
    LiveTradingStatus,
    LiveTradingResult,
)
from live_trading.live_portfolio import LivePortfolioManager


class LiveTradingEngine:
    """
    Master controller for Live Trading.
    """

    def __init__(self):

        self.portfolio = LivePortfolioManager()

    def initialize(self):

        portfolio = self.portfolio.portfolio()

        status = LiveTradingStatus(
            running=True,
            account_balance=portfolio.balance,
            total_positions=0,
        )

        result = LiveTradingResult(
            approved=True,
            reason="Live trading engine initialized successfully.",
            status=status,
        )

        LiveLogger.log(result)

        return result