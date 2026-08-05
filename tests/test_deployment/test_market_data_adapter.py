"""
=================================================
Project Phoenix
Market Data Adapter Test
M58.12.5
=================================================
"""

from deployment.live_market_data import (
    LiveMarketData,
)

from deployment.market_data_adapter import (
    MarketDataAdapter,
)


def test_market_data_adapter():

    market = LiveMarketData()

    assert market.connect()

    candles = market.get_candles(

        symbol="EURUSD",

        timeframe="M15",

        bars=10,

    )

    adapter = MarketDataAdapter()

    normalized = adapter.normalize(
        candles
    )

    assert isinstance(
        normalized,
        list,
    )

    assert len(
        normalized,
    ) > 0

    first = normalized[0]

    assert isinstance(
        first,
        dict,
    )

    assert "open" in first

    assert "high" in first

    assert "low" in first

    assert "close" in first

    market.disconnect()