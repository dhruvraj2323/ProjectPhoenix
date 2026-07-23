"""
=================================================
Project Phoenix
Test Signal Manager
M34
=================================================
"""

from signal_engine.signal_context import SignalContext
from signal_engine.signal_manager import SignalManager


def test_signal_manager():

    manager = SignalManager()

    context = SignalContext(
        engine_id="SIGNAL-001",
        symbol="XAUUSD",
        timeframe="M1",
    )

    context.patterns = [
        {"name": "DOJI"}
    ]

    context.indicators = {
        "EMA20": 100,
    }

    result = manager.execute(context)

    assert result.completed is True
    assert result.failed is False