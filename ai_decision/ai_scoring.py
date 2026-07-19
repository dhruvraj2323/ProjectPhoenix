"""
Project Phoenix
Milestone M14 - AI Decision Engine

Module:
    ai_scoring.py

Purpose:
    Calculates final AI decision score.
"""

from __future__ import annotations

from ai_decision.ai_models import (
    AIRecommendation,
)


class AIScoring:
    """
    Calculates AI decision score.
    """

    def calculate(
        self,
        recommendation: AIRecommendation,
    ) -> float:
        """
        Return the final AI score.

        Placeholder implementation for M14.
        """

        return round(
            recommendation.score,
            2,
        )