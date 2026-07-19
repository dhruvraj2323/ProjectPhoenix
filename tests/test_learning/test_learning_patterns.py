"""
Project Phoenix

Unit Test
Learning Pattern Detector
"""

from learning.learning_models import (
    LearningContext,
)

from learning.learning_patterns import (
    LearningPatternDetector,
)


def test_learning_patterns():

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

    print("===== Learning Pattern =====")

    print(
        f"Pattern      : {pattern.pattern_name}"
    )

    print(
        f"Confidence   : {pattern.confidence}"
    )

    print(
        f"Occurrences  : {pattern.occurrences}"
    )

    print(
        f"Description  : {pattern.description}"
    )

    assert pattern.pattern_name == "High Win Rate"

    assert pattern.occurrences == 250

    print("\nLearning Pattern Test Passed")


if __name__ == "__main__":

    test_learning_patterns()