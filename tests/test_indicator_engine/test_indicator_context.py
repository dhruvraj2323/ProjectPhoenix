"""
=================================================
Project Phoenix
Indicator Context Test
M32
=================================================
"""

from indicator_engine.indicator_context import (
    IndicatorContext,
)


def test_indicator_context():

    context = IndicatorContext(
        engine_id="IND-001",
        symbol="XAUUSD",
        timeframe="M1",
    )

    context.add_indicator(
        "EMA20",
        3354.42,
    )

    context.add_indicator(
        "RSI14",
        57.84,
    )

    context.set_metadata(
        "Source",
        "Market Pipeline",
    )

    assert context.get_indicator("EMA20") == 3354.42
    assert context.get_indicator("RSI14") == 57.84

    assert (
        context.get_metadata("Source")
        == "Market Pipeline"
    )

    context.approve(
        decision="SUCCESS",
        reason="Indicator calculation completed.",
    )

    assert context.approved is True
    assert context.completed is True
    assert context.failed is False

    context.reset()

    assert context.indicators == {}
    assert context.metadata == {}

    assert context.approved is False
    assert context.completed is False
    assert context.failed is False

    print("===== Indicator Context =====")
    print("Engine ID :", context.engine_id)
    print("Symbol    :", context.symbol)
    print("Timeframe :", context.timeframe)
    print()

    print("Indicator Context Test Passed")


if __name__ == "__main__":
    test_indicator_context()