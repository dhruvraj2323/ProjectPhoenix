"""
Project Phoenix
Milestone M11 - Performance Feedback Engine

Module:
    performance_engine.py

Purpose:
    Coordinates the complete Performance Feedback Engine.
"""

from __future__ import annotations

from performance.performance_analyzer import PerformanceAnalyzer
from performance.performance_logger import PerformanceLogger
from performance.performance_models import (
    PerformanceContext,
    PerformanceDecision,
    PerformanceDecisionType,
)
from performance.performance_validator import PerformanceValidator


class PerformanceEngine:
    """
    Coordinates the complete Performance Feedback Engine.
    """

    def __init__(self) -> None:
        self._analyzer = PerformanceAnalyzer()
        self._validator = PerformanceValidator()
        self._logger = PerformanceLogger()

    def evaluate(
        self,
        context: PerformanceContext,
    ) -> PerformanceDecision:
        """
        Analyze completed trades and return the final decision.
        """

        metrics = self._analyzer.analyze(context)

        validation = self._validator.validate(metrics)

        if not validation.valid:
            self._logger.log(metrics)

            return PerformanceDecision(
                decision=PerformanceDecisionType.REVIEW,
                metrics=metrics,
                approved=False,
                reason=validation.reason,
            )

        self._logger.log(metrics)

        return PerformanceDecision(
            decision=PerformanceDecisionType.ACCEPT,
            metrics=metrics,
            approved=True,
            reason=validation.reason,
        )

        return PerformanceDecision(
            decision=PerformanceDecisionType.REVIEW,
            metrics=metrics,
            approved=False,
            reason=validation.reason,
        )