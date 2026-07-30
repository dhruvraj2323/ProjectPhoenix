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

    context.approve(
        decision="SIGNALS_GENERATED",
        reason="Signal generation completed successfully.",
    )

    logger.log_finish(context)

    assert context.completed is True
    assert context.approved is True
    assert context.failed is False
    assert context.decision == "SIGNALS_GENERATED"

    context.reject(
        decision="SIGNAL_VALIDATION_FAILED",
        reason="Validation Failed",
    )

    logger.log_failure(context)

    assert context.failed is True
    assert context.completed is True
    assert context.approved is False
    assert context.decision == "SIGNAL_VALIDATION_FAILED"
    assert context.reason == "Validation Failed"


if __name__ == "__main__":
    test_signal_logger()