"""
=================================================
Project Phoenix
Test Signal Processor
M34
=================================================
"""

from signal_engine.signal_context import (
    SignalContext,
)

from signal_engine.signal_processor import (
    SignalProcessor,
)


def test_signal_processor():

    processor = SignalProcessor()

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
            "strength": 1.0,
        }
    ]

    result = processor.process(
        context
    )

    assert result.get_signal_count() == 1

    signal = result.signals[0]

    assert signal["direction"] == "BUY"
    assert signal["strength"] == "STRONG"