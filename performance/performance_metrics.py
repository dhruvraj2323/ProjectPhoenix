"""
Project Phoenix
Milestone M11 - Performance Feedback Engine

Module:
    performance_metrics.py

Purpose:
    Calculates performance statistics from completed trades.
"""

from __future__ import annotations

from performance.performance_models import (
    PerformanceMetrics,
    PerformanceContext,
    TradeOutcome,
)


class PerformanceMetricsCalculator:
    """
    Calculates trading performance metrics.
    """

    def calculate(
        self,
        context: PerformanceContext,
    ) -> PerformanceMetrics:
        """
        Calculate basic performance metrics.
        """

        total = len(context.trades)

        wins = sum(
            1
            for trade in context.trades
            if trade.outcome == TradeOutcome.WIN
        )

        losses = sum(
            1
            for trade in context.trades
            if trade.outcome == TradeOutcome.LOSS
        )

        breakeven = sum(
            1
            for trade in context.trades
            if trade.outcome == TradeOutcome.BREAKEVEN
        )

        win_rate = (wins / total * 100.0) if total > 0 else 0.0

        profits = [
            trade.profit_loss
            for trade in context.trades
            if trade.profit_loss > 0
        ]

        losses_list = [
            trade.profit_loss
            for trade in context.trades
            if trade.profit_loss < 0
        ]

        average_profit = (
            sum(profits) / len(profits)
            if profits
            else 0.0
        )

        average_loss = (
            sum(losses_list) / len(losses_list)
            if losses_list
            else 0.0
        )

        return PerformanceMetrics(
            total_trades=total,
            wins=wins,
            losses=losses,
            breakeven=breakeven,
            win_rate=win_rate,
            average_profit=average_profit,
            average_loss=average_loss,
        )