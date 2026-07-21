"""
Project Phoenix
Milestone M16 - Backtesting Engine

Module:
    backtest_simulator.py

Purpose:
    Simulates historical trades.
"""

from __future__ import annotations

from backtesting.backtest_models import (
    BacktestContext,
    BacktestTrade,
)


class BacktestSimulator:
    """
    Simulates historical trades.
    """

    def simulate(
        self,
        context: BacktestContext,
    ) -> list[BacktestTrade]:
        """
        Execute placeholder backtest simulation.

        TODO (M16.1):
        Replace placeholder trades with
        historical market simulation.
        """

        trades = [

            BacktestTrade(

                symbol=context.symbol,

                entry_price=2500.0,

                exit_price=2550.0,

                volume=10.0,

                profit=500.0,

                win=True,

            ),

            BacktestTrade(

                symbol=context.symbol,

                entry_price=2550.0,

                exit_price=2525.0,

                volume=8.0,

                profit=-200.0,

                win=False,

            ),

            BacktestTrade(

                symbol=context.symbol,

                entry_price=2525.0,

                exit_price=2585.0,

                volume=10.0,

                profit=600.0,

                win=True,

            ),

        ]

        return trades