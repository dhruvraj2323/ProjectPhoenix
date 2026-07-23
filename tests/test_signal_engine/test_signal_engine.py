"""
=================================================
Project Phoenix
Test Signal Engine
M34
=================================================
"""

from signal_engine.signal_context import (
    SignalContext,
)
from signal_engine.signal_engine import (
    SignalEngine,
)


def test_signal_engine():

    engine = SignalEngine()

    context = SignalContext(
        engine_id="SIG-001",
        symbol="XAUUSD",
        timeframe="M1",
    )

    context.indicators = {
        "SMA": 100,
        "EMA": 105,
    }

    context.patterns = [
        {
            "name": "DOJI",
        }
    ]

    result = engine.run(
        context
    )

    assert result.completed is True
    assert result.failed is False
    assert result.get_signal_count() == 1