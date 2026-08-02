"""
=================================================
Project Phoenix
Position Monitor Test
M55
=================================================
"""

from live_trading.live_context import LiveContext
from live_trading.live_models import (
    LivePosition,
)
from live_trading.position_monitor import (
    PositionMonitor,
)


def test_position_monitor():

    context = LiveContext(
        live_id="LIVE-001",
        account_id="ACC-001",
        symbol="EURUSD",
        timeframe="M1",
    )

    context.position = LivePosition(
        position_id="POS-001",
        symbol="EURUSD",
        volume=0.10,
        entry_price=1.1050,
    )

    monitor = PositionMonitor()

    position = monitor.get_position(context)

    assert position is not None

    assert position.position_id == "POS-001"

    assert position.symbol == "EURUSD"