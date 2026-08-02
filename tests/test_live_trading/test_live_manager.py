"""
=================================================
Project Phoenix
Live Trading Manager Test
M55
=================================================
"""

from live_trading.live_context import LiveContext
from live_trading.live_manager import LiveManager


def test_live_manager():

    manager = LiveManager()

    context = LiveContext(
        live_id="LIVE-001",
        account_id="ACC-001",
        symbol="EURUSD",
        timeframe="M1",
    )

    context.market_price = 1.1050

    result = manager.run(context)

    assert result.completed

    assert not result.failed