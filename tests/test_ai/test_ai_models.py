"""
Project Phoenix

Unit Test
AI Models
"""

from ai_decision.ai_models import (
    AIContext,
    AIRecommendation,
    AIDecision,
    AIDecisionStatus,
)


def test_ai_models():

    context = AIContext(
        signal_strength=82.5,
        risk_score=18.0,
        performance_score=74.0,
        portfolio_score=91.0,
        optimization_score=86.0,
    )

    recommendation = AIRecommendation(
        decision=AIDecisionStatus.APPROVE,
        confidence=0.93,
        score=88.5,
        reason="Unit Test",
    )

    decision = AIDecision(
        recommendation=recommendation,
        approved=True,
        reason="AI Approved",
    )

    assert context.signal_strength == 82.5

    assert recommendation.confidence == 0.93

    assert decision.approved is True

    print("AI Models Test Passed")


if __name__ == "__main__":

    test_ai_models()