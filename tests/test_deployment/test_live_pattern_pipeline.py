"""
=================================================
Project Phoenix
Live Pattern Pipeline Test
M58.12.5
=================================================
"""

from deployment.live_pattern_pipeline import (
    LivePatternPipeline,
)


def test_live_pattern_pipeline():

    pipeline = LivePatternPipeline()

    result = pipeline.execute(

        symbol="EURUSD",

        timeframe="M15",

        bars=200,

    )

    assert result is not None

    assert result.approved is True

    assert isinstance(

        result.patterns,

        list,

    )

    print()

    print("===== Live Pattern Pipeline =====")

    print("Symbol      :", result.symbol)

    print("Timeframe   :", result.timeframe)

    print("Candles     :", len(result.candles))

    print("Patterns    :", len(result.patterns))

    print("Approved    :", result.approved)

    print()