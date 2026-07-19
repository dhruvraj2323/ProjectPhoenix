"""
Project Phoenix
Milestone M16 - Backtesting Engine

Module:
    backtest_logger.py

Purpose:
    Logs backtesting results.
"""

from __future__ import annotations

from backtesting.backtest_models import (
    BacktestDecision,
)


class BacktestLogger:
    """
    Logs Backtesting Engine decisions.
    """

    def log(
        self,
        decision: BacktestDecision,
    ) -> None:
        """
        Log backtesting decision.
        """

        print("===== Backtest =====")

        print(
            f"Status          : {decision.status.value}"
        )

        print(
            f"Approved        : {decision.approved}"
        )

        print(
            f"Total Trades    : "
            f"{decision.statistics.total_trades}"
        )

        print(
            f"Win Rate        : "
            f"{decision.statistics.win_rate:.2f}%"
        )

        print(
            f"Net Profit      : "
            f"{decision.statistics.net_profit}"
        )

        print(
            f"Profit Factor   : "
            f"{decision.statistics.profit_factor:.2f}"
        )

        print(
            f"Drawdown        : "
            f"{decision.statistics.max_drawdown:.2f}%"
        )

        print(
            f"Expectancy      : "
            f"{decision.statistics.expectancy:.2f}"
        )

        print(
            f"Reason          : "
            f"{decision.reason}"
        )