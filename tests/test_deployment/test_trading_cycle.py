"""
=================================================
Project Phoenix
Trading Cycle Test
M58
=================================================
"""

from deployment.trading_cycle import (
    TradingCycle,
)


def test_trading_cycle():

    cycle = TradingCycle()

    assert cycle.execute() is True