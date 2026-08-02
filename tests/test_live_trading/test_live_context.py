"""
=================================================
Project Phoenix
Live Trading Context Test
M55
=================================================
"""

from live_trading.live_context import LiveContext


def test_live_context():

    context = LiveContext(
        live_id="LIVE-001",
        account_id="ACC-001",
        symbol="EURUSD",
        timeframe="M1",
    )

    assert context.live_id == "LIVE-001"
    assert context.account_id == "ACC-001"
    assert context.symbol == "EURUSD"
    assert context.timeframe == "M1"

    context.set_metadata(
        "broker",
        "MT5",
    )

    assert context.metadata["broker"] == "MT5"

    context.complete()

    assert context.completed
    assert not context.failed

    context.fail("Connection lost")

    assert context.failed
    assert context.reason == "Connection lost"

    context.reset()

    assert context.order is None
    assert context.position is None
    assert context.trade is None
    assert context.market_price == 0.0
    assert context.spread == 0.0
    assert not context.completed
    assert not context.failed
    assert context.reason == ""
    assert context.metadata == {}