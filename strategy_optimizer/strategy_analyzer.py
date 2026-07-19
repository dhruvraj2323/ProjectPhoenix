"""
Project Phoenix
Milestone M13 - Strategy Optimizer Engine

Module:
    strategy_analyzer.py

Purpose:
    Analyzes strategy performance and prepares
    optimization inputs.
"""

from __future__ import annotations

from strategy_optimizer.strategy_models import (
    StrategyContext,
    StrategyPerformance,
)


class StrategyAnalyzer:
    """
    Analyzes strategy performance.
    """

    def analyze(
        self,
        context: StrategyContext,
    ) -> StrategyPerformance:
        """
        Return strategy performance.

        M13 V1.0 simply returns the supplied
        performance object.
        """

        return context.performance