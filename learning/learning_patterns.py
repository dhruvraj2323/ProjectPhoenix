"""
Project Phoenix
Milestone M17 - Learning Engine

Module:
    learning_patterns.py

Purpose:
    Detects trading patterns from historical
    performance.
"""

from __future__ import annotations

from learning.learning_models import (
    LearningContext,
    LearningPattern,
)


class LearningPatternDetector:
    """
    Detects trading patterns.
    """

    def detect(
        self,
        context: LearningContext,
    ) -> LearningPattern:
        """
        Detect learning pattern.
        """

        if (
            context.win_rate >= 60.0
            and
            context.profit_factor >= 1.50
        ):

            pattern_name = "High Win Rate"

            confidence = 0.92

            description = (
                "Consistently profitable trading "
                "behavior detected."
            )

        else:

            pattern_name = "Low Win Rate"

            confidence = 0.65

            description = (
                "Performance improvement required."
            )

        return LearningPattern(

            pattern_name=pattern_name,

            confidence=confidence,

            occurrences=context.total_trades,

            description=description,

        )