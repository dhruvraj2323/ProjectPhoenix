"""
Project Phoenix

Unit Test
AI Logger
"""

from ai_decision.ai_logger import (
    AILogger,
)

from ai_decision.ai_models import (
    AIRecommendation,
    AIDecision,
    AIDecisionStatus,
)


def test_ai_logger():

    recommendation = AIRecommendation(

        decision=AIDecisionStatus.APPROVE,

        confidence=0.91,

        score=88.40,

        reason="AI Approved",

    )

    decision = AIDecision(

        recommendation=recommendation,

        approved=True,

        reason="AI validation passed.",

    )

    logger = AILogger()

    logger.log(
        decision
    )

    print("\nAI Logger Test Passed")


if __name__ == "__main__":

    test_ai_logger()