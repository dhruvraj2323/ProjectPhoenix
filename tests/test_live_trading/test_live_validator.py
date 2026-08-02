"""
=================================================
Project Phoenix
Live Trading Validator Test
M55
=================================================
"""

from live_trading.live_context import LiveContext
from live_trading.live_validator import LiveValidator


def test_live_validator():

    validator = LiveValidator()

    context = LiveContext(
        live_id="LIVE-001",
        account_id="ACC-001",
        symbol="EURUSD",
        timeframe="M1",
    )

    context.market_price = 1.1050

    assert validator.validate(context)

    bad_context = LiveContext(
        live_id="LIVE-002",
        account_id="ACC-001",
        symbol="",
        timeframe="M1",
    )

    bad_context.market_price = 1.1050

    assert not validator.validate(bad_context)

    assert bad_context.failed

    assert bad_context.reason == "Missing trading symbol."