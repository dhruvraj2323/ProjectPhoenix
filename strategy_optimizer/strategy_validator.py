"""
Project Phoenix
Milestone M13 - Strategy Optimizer Engine

Module:
    strategy_validator.py

Purpose:
    Validates optimization recommendations before
    they are approved.
"""

from __future__ import annotations

from dataclasses import dataclass

from strategy_optimizer.strategy_models import (
    OptimizationRecommendation,
)


@dataclass
class StrategyValidationResult:
    """
    Result returned by the Strategy Validator.
    """

    valid: bool

    reason: str


class StrategyValidator:
    """
    Validates optimization recommendations.
    """

    def validate(
        self,
        recommendation: OptimizationRecommendation,
    ) -> StrategyValidationResult:
        """
        Validate optimization recommendation.
        """

        if recommendation.confidence < 0.50:

            return StrategyValidationResult(
                valid=False,
                reason="Optimization confidence below minimum threshold.",
            )

        if recommendation.suggested_value < 0:

            return StrategyValidationResult(
                valid=False,
                reason="Suggested value cannot be negative.",
            )    

        return StrategyValidationResult(
            valid=True,
            reason="Strategy optimization validation passed.",
        )