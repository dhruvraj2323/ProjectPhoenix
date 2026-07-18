"""
Project Phoenix
Milestone M11 - Performance Feedback Engine

Module:
    performance_logger.py

Purpose:
    Logs performance metrics.
"""

from __future__ import annotations

from performance.performance_models import PerformanceMetrics


class PerformanceLogger:
    """
    Logs calculated performance metrics.
    """

    def log(
        self,
        metrics: PerformanceMetrics,
    ) -> None:
        """
        Log performance metrics.
        """

        print("===== Performance Summary =====")
        print(f"Total Trades   : {metrics.total_trades}")
        print(f"Wins           : {metrics.wins}")
        print(f"Losses         : {metrics.losses}")
        print(f"Breakeven      : {metrics.breakeven}")
        print(f"Win Rate       : {metrics.win_rate:.2f}%")
        print(f"Average Profit : {metrics.average_profit}")
        print(f"Average Loss   : {metrics.average_loss}")