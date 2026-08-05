"""
=================================================
Project Phoenix
Live Market Data Test
M58.12.1
=================================================
"""

from deployment.live_market_data import (
    LiveMarketData,
)


def test_live_market_data():

    market = LiveMarketData()

    assert market.connect()

    data = market.get_multi_timeframe_data(
        symbol="EURUSD",
        bars=10,
    )

    assert "D1" in data

    assert "H4" in data

    assert "H1" in data

    assert "M15" in data

    assert "M5" in data

    assert len(data["D1"]) > 0

    market.disconnect()