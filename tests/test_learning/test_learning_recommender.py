"""
Project Phoenix

Unit Test
Learning Recommender
"""

from learning.learning_models import (
    LearningContext,
)

from learning.learning_patterns import (
    LearningPatternDetector,
)

from learning.learning_recommender import (
    LearningRecommender,
)


def test_learning_recommender():

    context = LearningContext(

        strategy_name="Phoenix Strategy",

        total_trades=250,

        win_rate=64.5,

        profit_factor=2.15,

    )

    detector = LearningPatternDetector()

    pattern = detector.detect(
        context
    )

    recommender = LearningRecommender()

    recommendation = recommender.recommend(
        pattern
    )

    print("===== Learning Recommendation =====")

    print(
        f"Type         : "
        f"{recommendation.recommendation_type}"
    )

    print(
        f"Current      : "
        f"{recommendation.current_value}"
    )

    print(
        f"Suggested    : "
        f"{recommendation.suggested_value}"
    )

    print(
        f"Confidence   : "
        f"{recommendation.confidence}"
    )

    print(
        f"Reason       : "
        f"{recommendation.reason}"
    )

    assert recommendation.suggested_value == 1.2

    print("\nLearning Recommender Test Passed")


if __name__ == "__main__":

    test_learning_recommender()