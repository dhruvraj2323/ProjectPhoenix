"""
=================================================
Project Phoenix
Trading Context Test
=================================================
"""

from trading_system.trading_context import (
    TradingContext,
)


def test_trading_context():

    context = TradingContext(

        trading_id="TRD-001",

        symbol="XAUUSD",

        timeframe="M1",

    )

    context.add_indicator(
        "EMA20",
        3354.21,
    )

    context.add_pattern(
        "Bullish Engulfing",
        True,
    )

    context.set_metadata(
        "Source",
        "Market Pipeline",
    )

    assert context.get_indicator("EMA20") == 3354.21

    assert context.get_pattern(
        "Bullish Engulfing"
    ) is True

    assert (
        context.get_metadata("Source")
        == "Market Pipeline"
    )

    context.approve(

        decision="BUY",

        reason="Trading flow completed.",

    )

    assert context.approved is True

    assert context.decision == "BUY"

    print()

    print("Trading Context Test Passed")


if __name__ == "__main__":

    test_trading_context()