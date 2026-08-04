"""
=================================================
Project Phoenix
Market Data Feed Test
M58
=================================================
"""

from deployment.market_data_feed import (
    MarketDataFeed,
)


def test_market_data_feed():

    feed = MarketDataFeed()

    data = feed.fetch()

    assert "D1" in data

    assert "H4" in data

    assert "H1" in data

    assert "M15" in data

    assert "M5" in data