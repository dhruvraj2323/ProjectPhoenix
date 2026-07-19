"""
Project Phoenix
Milestone M17 - Learning Engine

Module:
    learning_validator.py

Purpose:
    Validates learning recommendations.
"""

from __future__ import annotations

from dataclasses import dataclass

from learning.learning_models import (
    LearningRecommendation,
)


@dataclass
class LearningValidationResult:
    """
    Result returned by the Learning Validator.
    """

    valid: bool

    reason: str


class LearningValidator:
    """
    Validates learning recommendations.
    """

    def validate(
        self,
        recommendation: LearningRecommendation,
    ) -> LearningValidationResult:
        """
        Validate recommendation.
        """

        if not (
            0.0
            <= recommendation.confidence
            <= 1.0
        ):

            return LearningValidationResult(

                valid=False,

                reason="Invalid confidence value.",

            )

        if recommendation.suggested_value <= 0:

            return LearningValidationResult(

                valid=False,

                reason="Suggested value must be positive.",

            )

        if not recommendation.reason.strip():

            return LearningValidationResult(

                valid=False,

                reason="Recommendation reason is required.",

            )

        return LearningValidationResult(

            valid=True,

            reason="Learning recommendation validation passed.",

        )