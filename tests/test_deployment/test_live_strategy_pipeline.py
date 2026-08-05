"""
=================================================
Project Phoenix
Live Strategy Pipeline Test
M58.12.6
=================================================
"""

from deployment.live_strategy_pipeline import (
    LiveStrategyPipeline,
)


def test_live_strategy_pipeline():

    pipeline = LiveStrategyPipeline()

    result = pipeline.execute(

        symbol="EURUSD",

        timeframe="M15",

        bars=200,

    )

    assert result is not None

    assert result.completed is True

    assert result.failed is False

    assert result.strategy_result is not None

    assert len(
        result.strategy_result.signals
    ) >= 0

    print()

    print("===== Live Strategy =====")

    print("Symbol :", result.symbol)

    print("TF     :", result.timeframe)

    print(
        "Signals:",
        len(
            result.strategy_result.signals
        ),
    )

    print(
        "Status :",
        result.strategy_result.status,
    )

    print()