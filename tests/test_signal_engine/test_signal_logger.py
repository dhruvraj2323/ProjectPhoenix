"""
=================================================
Project Phoenix
Test Signal Logger
M34
=================================================
"""

from signal_engine.signal_context import (
    SignalContext,
)

from signal_engine.signal_logger import (
    SignalLogger,
)


def test_signal_logger():

    logger = SignalLogger()

    context = SignalContext(
        engine_id="SIG-001",
        symbol="XAUUSD",
        timeframe="M1",
    )

    context.add_signal(
        {
            "direction": "BUY",
            "strength": "STRONG",
        }
    )

    logger.log_start(context)

    context.mark_completed()

    logger.log_finish(context)

    context.mark_failed(
        "Validation Failed"
    )

    logger.log_failure(context)

    assert context.failed is True
    assert context.reason == "Validation Failed"