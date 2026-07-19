"""
Project Phoenix

Unit Test
AI Scoring
"""

from ai_decision.ai_models import (
    AIRecommendation,
    AIDecisionStatus,
)

from ai_decision.ai_scoring import (
    AIScoring,
)


def test_ai_scoring():

    recommendation = AIRecommendation(

        decision=AIDecisionStatus.APPROVE,

        confidence=0.91,

        score=87.45,

        reason="Unit Test",

    )

    scoring = AIScoring()

    score = scoring.calculate(
        recommendation
    )

    print("===== AI Scoring =====")
    print(f"Decision : {recommendation.decision.value}")
    print(f"Score    : {score}")

    assert score == 87.45

    print("\nAI Scoring Test Passed")


if __name__ == "__main__":

    test_ai_scoring()