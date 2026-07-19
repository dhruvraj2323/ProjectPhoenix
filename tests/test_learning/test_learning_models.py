"""
Project Phoenix

Unit Test
Learning Models
"""

from learning.learning_models import (
    LearningContext,
    LearningDecision,
    LearningPattern,
    LearningRecommendation,
    LearningStatus,
)


def test_learning_models():

    pattern = LearningPattern(

        pattern_name="High Win Rate",

        confidence=0.91,

        occurrences=45,

        description="Strong performance detected.",

    )

    recommendation = LearningRecommendation(

        recommendation_type="RISK_PERCENT",

        current_value=1.0,

        suggested_value=1.2,

        confidence=0.88,

        reason="Increase position sizing.",

    )

    context = LearningContext(

        strategy_name="Phoenix Strategy",

        total_trades=250,

        win_rate=64.5,

        profit_factor=2.15,

    )

    decision = LearningDecision(

        status=LearningStatus.APPROVED,

        pattern=pattern,

        recommendation=recommendation,

        approved=True,

        reason="Learning completed successfully.",

    )

    assert pattern.occurrences == 45

    assert recommendation.suggested_value == 1.2

    assert context.total_trades == 250

    assert decision.approved is True

    print("Learning Models Test Passed")


if __name__ == "__main__":

    test_learning_models()