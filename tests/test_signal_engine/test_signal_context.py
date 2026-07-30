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

    context.approve(
        decision="SIGNALS_GENERATED",
        reason="Signal generation completed successfully.",
    )

    assert context.completed is True
    assert context.approved is True
    assert context.failed is False
    assert context.decision == "SIGNALS_GENERATED"
    assert context.reason == "Signal generation completed successfully."

    context.reset()

    assert context.get_signal_count() == 0
    assert context.completed is False
    assert context.approved is False
    assert context.failed is False
    assert context.decision == ""
    assert context.reason == ""

    context.reject(
        decision="SIGNAL_VALIDATION_FAILED",
        reason="Validation Failed",
    )

    assert context.failed is True
    assert context.completed is True
    assert context.approved is False
    assert context.decision == "SIGNAL_VALIDATION_FAILED"
    assert context.reason == "Validation Failed"


if __name__ == "__main__":
    test_signal_context()