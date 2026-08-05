"""
=================================================
Project Phoenix
Live Indicator Pipeline Test
M58.12.4
=================================================
"""

from deployment.live_indicator_pipeline import (
    LiveIndicatorPipeline,
)


def test_live_indicator_pipeline():

    pipeline = LiveIndicatorPipeline()

    result = pipeline.execute(

        symbol="EURUSD",

        timeframe="M15",

        bars=200,

    )

    assert result is not None

    assert result.approved is True

    assert isinstance(

        result.indicators,

        dict,

    )

    assert len(

        result.indicators,

    ) > 0

    print()

    print("===== Live Indicator Pipeline =====")

    print("Symbol      :", result.symbol)

    print("Timeframe   :", result.timeframe)

    print("Candles     :", len(result.candles))

    print("Indicators  :", len(result.indicators))

    print("Approved    :", result.approved)

    print()