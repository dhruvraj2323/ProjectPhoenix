"""
Project Phoenix

Unit Test
Learning Validator
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

from learning.learning_validator import (
    LearningValidator,
)


def test_learning_validator():

    context = LearningContext(

        strategy_name="Phoenix Strategy",

        total_trades=250,

        win_rate=64.5,

        profit_factor=2.15,

    )

    pattern = (

        LearningPatternDetector()

        .detect(
            context
        )

    )

    recommendation = (

        LearningRecommender()

        .recommend(
            pattern
        )

    )

    validator = LearningValidator()

    result = validator.validate(
        recommendation
    )

    print("===== Learning Validator =====")

    print(
        f"Valid  : {result.valid}"
    )

    print(
        f"Reason : {result.reason}"
    )

    assert result.valid is True

    print("\nLearning Validator Test Passed")


if __name__ == "__main__":

    test_learning_validator()