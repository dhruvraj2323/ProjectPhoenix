from strategy.strategy_scoring import (
    StrategyScoring,
)


def test_strategy_scoring():

    scoring = StrategyScoring()

    patterns = [

        {
            "strength": 5.0,
            "confirmed": True,
            "confirmation_score": 2.0,
        }

    ]

    indicators = {

        "EMA9": 20,

        "EMA21": 15,

        "EMA200": 10,

        "RSI14": 60,

    }

    pattern_score = scoring.calculate_pattern_score(
        patterns,
    )

    indicator_score = scoring.calculate_indicator_score(
        indicators,
    )

    confirmation_score = (
        scoring.calculate_confirmation_score(
            patterns,
        )
    )

    strategy_score = (
        scoring.calculate_strategy_score(
            pattern_score,
            indicator_score,
            confirmation_score,
        )
    )

    confidence = scoring.calculate_confidence(
        strategy_score,
    )

    assert pattern_score > 0

    assert indicator_score > 0

    assert confirmation_score > 0

    assert strategy_score > 0

    assert confidence > 0