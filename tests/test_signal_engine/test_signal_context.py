"""
=================================================
Project Phoenix
Test Signal Context
M34
=================================================
"""

from signal_engine.signal_context import (
    SignalContext,
)


def test_signal_context():

    context = SignalContext(
        engine_id="SIG-001",
        symbol="XAUUSD",
        timeframe="M1",
    )

    assert context.symbol == "XAUUSD"
    assert context.timeframe == "M1"

    context.add_signal(
        {
            "direction": "BUY",
            "strength": "STRONG",
        }
    )

    assert context.get_signal_count() == 1

    context.mark_completed()

    assert context.completed is True

    context.reset()

    assert context.get_signal_count() == 0
    assert context.completed is False

    context.mark_failed(
        "Validation Failed"
    )

    assert context.failed is True
    assert context.reason == "Validation Failed"