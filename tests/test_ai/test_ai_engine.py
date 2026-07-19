"""
Project Phoenix

Unit Test
AI Engine
"""

from ai_decision.ai_engine import (
    AIEngine,
)

from ai_decision.ai_models import (
    AIContext,
)


def test_ai_engine():

    context = AIContext(

        signal_strength=84.0,

        risk_score=18.0,

        performance_score=79.0,

        portfolio_score=91.0,

        optimization_score=85.0,

    )

    engine = AIEngine()

    decision = engine.evaluate(
        context
    )

    print("\n===== AI Engine =====")

    print(
        f"Decision : "
        f"{decision.recommendation.decision.value}"
    )

    print(
        f"Approved : "
        f"{decision.approved}"
    )

    print(
        f"Reason   : "
        f"{decision.reason}"
    )

    assert decision.approved is True

    print("\nAI Engine Test Passed")


if __name__ == "__main__":

    test_ai_engine()