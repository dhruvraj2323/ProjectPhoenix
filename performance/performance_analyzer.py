"""
Project Phoenix
Milestone M11 - Performance Feedback Engine

Module:
    performance_analyzer.py

Purpose:
    Analyzes completed trades and generates performance metrics.
"""

from __future__ import annotations

from performance.performance_metrics import PerformanceMetricsCalculator
from performance.performance_models import (
    PerformanceContext,
    PerformanceMetrics,
)


class PerformanceAnalyzer:
    """
    Performs performance analysis on completed trades.
    """

    def __init__(self) -> None:
        self._calculator = PerformanceMetricsCalculator()

    def analyze(
        self,
        context: PerformanceContext,
    ) -> PerformanceMetrics:
        """
        Analyze completed trades and return performance metrics.
        """

        return self._calculator.calculate(context)