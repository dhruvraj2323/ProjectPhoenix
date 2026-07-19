"""
Project Phoenix

Unit Test
Learning Logger
"""

from learning.learning_logger import (
    LearningLogger,
)

from learning.learning_models import (
    LearningContext,
    LearningDecision,
    LearningStatus,
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


def test_learning_logger():

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

    validation = (

        LearningValidator()

        .validate(
            recommendation
        )

    )

    decision = LearningDecision(

        status=(
            LearningStatus.APPROVED
            if validation.valid
            else LearningStatus.REJECTED
        ),

        pattern=pattern,

        recommendation=recommendation,

        approved=validation.valid,

        reason=validation.reason,

    )

    logger = LearningLogger()

    logger.log(
        decision
    )

    print("\nLearning Logger Test Passed")


if __name__ == "__main__":

    test_learning_logger()