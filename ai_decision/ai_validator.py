"""
Project Phoenix
Milestone M14 - AI Decision Engine

Module:
    ai_validator.py

Purpose:
    Validates AI recommendations before
    final approval.
"""

from __future__ import annotations

from dataclasses import dataclass

from ai_decision.ai_models import (
    AIRecommendation,
)


@dataclass
class AIValidationResult:
    """
    Result returned by the AI Validator.
    """

    valid: bool

    reason: str


class AIValidator:
    """
    Validates AI recommendations.
    """

    def validate(
        self,
        recommendation: AIRecommendation,
    ) -> AIValidationResult:
        """
        Validate AI recommendation.
        """

        if recommendation.confidence <= 0.0:
            return AIValidationResult(
                valid=False,
                reason="Confidence must be greater than zero.",
            )

        if recommendation.score < 0.0:
            return AIValidationResult(
                valid=False,
                reason="Score cannot be negative.",
            )

        if recommendation.reason.strip() == "":
            return AIValidationResult(
                valid=False,
                reason="Reason cannot be empty.",
            )

        return AIValidationResult(
            valid=True,
            reason="AI recommendation validation passed.",
        )