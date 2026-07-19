"""
Project Phoenix

Unit Test
AI Validator
"""

from ai_decision.ai_models import (
    AIRecommendation,
    AIDecisionStatus,
)

from ai_decision.ai_validator import (
    AIValidator,
)


def test_ai_validator():

    recommendation = AIRecommendation(

        decision=AIDecisionStatus.APPROVE,

        confidence=0.88,

        score=84.50,

        reason="Unit Test",

    )

    validator = AIValidator()

    result = validator.validate(
        recommendation
    )

    print("===== AI Validator =====")
    print(f"Valid  : {result.valid}")
    print(f"Reason : {result.reason}")

    assert result.valid is True

    print("\nAI Validator Test Passed")


if __name__ == "__main__":

    test_ai_validator()