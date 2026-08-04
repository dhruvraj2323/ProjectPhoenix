"""
=================================================
Project Phoenix
Analytics Engine
M57
=================================================
"""

from __future__ import annotations

from reporting.reporting_models import (
    PerformanceSummary,
    TradeRecord,
)


class AnalyticsEngine:
    """
    Calculates trading statistics
    for daily reports.
    """

    def calculate(
        self,
        trades: list[TradeRecord],
    ) -> PerformanceSummary:
        """
        Generate performance summary
        from completed trades.
        """

        summary = PerformanceSummary()

        summary.total_trades = len(
            trades,
        )

        if not trades:

            return summary

        summary.winning_trades = sum(
            1
            for trade in trades
            if trade.profit_loss > 0
        )

        summary.losing_trades = sum(
            1
            for trade in trades
            if trade.profit_loss < 0
        )

        summary.gross_profit = sum(
            trade.profit_loss
            for trade in trades
            if trade.profit_loss > 0
        )

        summary.gross_loss = abs(
            sum(
                trade.profit_loss
                for trade in trades
                if trade.profit_loss < 0
            )
        )

        summary.net_profit = (
            summary.gross_profit
            - summary.gross_loss
        )

        if summary.total_trades > 0:

            summary.win_rate = (
                summary.winning_trades
                / summary.total_trades
            ) * 100.0

        if summary.winning_trades > 0:

            summary.average_profit = (
                summary.gross_profit
                / summary.winning_trades
            )

        if summary.losing_trades > 0:

            summary.average_loss = (
                summary.gross_loss
                / summary.losing_trades
            )

        if summary.gross_loss > 0:

            summary.profit_factor = (
                summary.gross_profit
                / summary.gross_loss
            )

        return summary