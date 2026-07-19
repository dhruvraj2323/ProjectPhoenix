"""
Project Phoenix
Milestone M17 - Learning Engine

Module:
    learning_logger.py

Purpose:
    Logs Learning Engine decisions.
"""

from __future__ import annotations

from learning.learning_models import (
    LearningDecision,
)


class LearningLogger:
    """
    Logs Learning Engine decisions.
    """

    def log(
        self,
        decision: LearningDecision,
    ) -> None:
        """
        Log learning decision.
        """

        print("===== Learning Engine =====")

        print(
            f"Status            : "
            f"{decision.status.value}"
        )

        print(
            f"Approved          : "
            f"{decision.approved}"
        )

        print(
            f"Pattern           : "
            f"{decision.pattern.pattern_name}"
        )

        print(
            f"Pattern Confidence: "
            f"{decision.pattern.confidence:.2f}"
        )

        print(
            f"Occurrences       : "
            f"{decision.pattern.occurrences}"
        )

        print(
            f"Recommendation    : "
            f"{decision.recommendation.recommendation_type}"
        )

        print(
            f"Current Value     : "
            f"{decision.recommendation.current_value}"
        )

        print(
            f"Suggested Value   : "
            f"{decision.recommendation.suggested_value}"
        )

        print(
            f"Recommendation Conf.: "
            f"{decision.recommendation.confidence:.2f}"
        )

        print(
            f"Reason            : "
            f"{decision.reason}"
        )