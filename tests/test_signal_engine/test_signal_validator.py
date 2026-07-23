"""
=================================================
Project Phoenix
Test Signal Validator
M34
=================================================
"""

from signal_engine.signal_context import (
    SignalContext,
)

from signal_engine.signal_validator import (
    SignalValidator,
)


def test_signal_validator():

    validator = SignalValidator()

    context = SignalContext(
        engine_id="SIG-001",
        symbol="XAUUSD",
        timeframe="M1",
    )

    context.indicators = {
        "SMA": 100,
        "EMA": 101,
    }

    context.patterns = [
        {
            "name": "DOJI",
        }
    ]

    assert validator.validate(context) is True

    invalid = SignalContext(
        engine_id="SIG-002",
        symbol="",
        timeframe="M1",
    )

    assert validator.validate(invalid) is False
    assert invalid.failed is True