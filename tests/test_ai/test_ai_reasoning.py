"""
Project Phoenix

Unit Test
AI Reasoning
"""

from ai_decision.ai_models import (
    AIContext,
)

from ai_decision.ai_reasoning import (
    AIReasoning,
)


def test_ai_reasoning():

    context = AIContext(

        signal_strength=85.0,

        risk_score=20.0,

        performance_score=78.0,

        portfolio_score=90.0,

        optimization_score=82.0,

    )

    reasoning = AIReasoning()

    recommendation = reasoning.evaluate(
        context
    )

    print("===== AI Reasoning =====")
    print(
        f"Decision   : {recommendation.decision.value}"
    )
    print(
        f"Confidence : {recommendation.confidence}"
    )
    print(
        f"Score      : {recommendation.score}"
    )
    print(
        f"Reason     : {recommendation.reason}"
    )

    assert recommendation.confidence > 0.0

    print("\nAI Reasoning Test Passed")


if __name__ == "__main__":

    test_ai_reasoning()