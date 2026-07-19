"""
Project Phoenix
Milestone M14 - AI Decision Engine

Module:
    ai_logger.py

Purpose:
    Logs AI decision results.
"""

from __future__ import annotations

from ai_decision.ai_models import (
    AIDecision,
)


class AILogger:
    """
    Logs AI Engine decisions.
    """

    def log(
        self,
        decision: AIDecision,
    ) -> None:
        """
        Log AI decision.
        """

        recommendation = decision.recommendation

        print("===== AI Decision =====")

        print(
            f"Decision          : "
            f"{recommendation.decision.value}"
        )

        print(
            f"Approved          : "
            f"{decision.approved}"
        )

        print(
            f"Confidence        : "
            f"{recommendation.confidence:.2f}"
        )

        print(
            f"Score             : "
            f"{recommendation.score:.2f}"
        )

        print(
            f"Reason            : "
            f"{decision.reason}"
        )