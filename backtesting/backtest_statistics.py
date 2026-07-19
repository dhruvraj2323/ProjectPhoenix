"""
Project Phoenix
Milestone M16 - Backtesting Engine

Module:
    backtest_statistics.py

Purpose:
    Calculates backtesting statistics.
"""

from __future__ import annotations

from backtesting.backtest_models import (
    BacktestStatistics,
    BacktestTrade,
)


class BacktestStatisticsCalculator:
    """
    Calculates backtesting statistics.
    """

    def calculate(
        self,
        trades: list[BacktestTrade],
    ) -> BacktestStatistics:
        """
        Calculate summary statistics.
        """

        total_trades = len(
            trades
        )

        winning_trades = sum(

            1

            for trade in trades

            if trade.win

        )

        total_profit = sum(

            trade.profit

            for trade in trades

            if trade.profit > 0

        )

        total_loss = abs(

            sum(

                trade.profit

                for trade in trades

                if trade.profit < 0

            )

        )

        net_profit = sum(

            trade.profit

            for trade in trades

        )

        if total_trades > 0:

            win_rate = (

                winning_trades

                /

                total_trades

            ) * 100

        else:

            win_rate = 0.0

        if total_loss > 0:

            profit_factor = (

                total_profit

                /

                total_loss

            )

        else:

            profit_factor = 0.0

        expectancy = (

            net_profit

            /

            total_trades

            if total_trades > 0

            else 0.0

        )

        return BacktestStatistics(

            total_trades=total_trades,

            win_rate=win_rate,

            net_profit=net_profit,

            profit_factor=profit_factor,

            max_drawdown=0.0,

            expectancy=expectancy,

        )