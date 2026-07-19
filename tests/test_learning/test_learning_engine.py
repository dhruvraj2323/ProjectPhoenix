"""
Project Phoenix

Unit Test
Learning Engine
"""

from learning.learning_engine import (
    LearningEngine,
)

from learning.learning_models import (
    LearningContext,
)


def test_learning_engine():

    context = LearningContext(

        strategy_name="Phoenix Strategy",

        total_trades=250,

        win_rate=64.5,

        profit_factor=2.15,

    )

    engine = LearningEngine()

    decision = engine.run(
        context
    )

    print("\n===== Learning Engine =====")

    print(
        f"Status   : {decision.status.value}"
    )

    print(
        f"Approved : {decision.approved}"
    )

    print(
        f"Reason   : {decision.reason}"
    )

    assert decision.approved is True

    print("\nLearning Engine Test Passed")


if __name__ == "__main__":

    test_learning_engine()