"""
Project Phoenix
Milestone M11 - Performance Feedback Engine

Module:
    performance_validator.py

Purpose:
    Validates calculated performance metrics.
"""

from __future__ import annotations

from dataclasses import dataclass

from performance.performance_models import PerformanceMetrics


@dataclass
class PerformanceValidationResult:
    """
    Result returned by the performance validator.
    """

    valid: bool

    reason: str


class PerformanceValidator:
    """
    Validates calculated performance metrics.
    """

    def validate(
        self,
        metrics: PerformanceMetrics,
    ) -> PerformanceValidationResult:
        """
        Validate performance metrics.
        """

        if metrics.total_trades < 1:
            return PerformanceValidationResult(
                valid=False,
                reason="No completed trades available.",
            )

        if not 0.0 <= metrics.win_rate <= 100.0:
            return PerformanceValidationResult(
                valid=False,
                reason="Invalid win rate.",
            )

        return PerformanceValidationResult(
            valid=True,
            reason="Performance validation passed.",
        )