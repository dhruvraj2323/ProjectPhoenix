"""
=================================================
Project Phoenix
Test Live Trade Context
M59.1.2
=================================================
"""

from live_execution.trade_context import (
    TradeContext,
)


def test_trade_context():

    context = TradeContext(

        execution_id="EXEC-001",

        symbol="EURUSD",

        timeframe="M15",

    )

    assert (
        context.completed
        is False
    )

    assert (
        context.failed
        is False
    )

    context.set_metadata(

        "broker",

        "MT5",

    )

    assert (

        context.get_metadata(
            "broker"
        )

        == "MT5"

    )

    context.complete()

    assert (
        context.completed
        is True
    )

    context.fail(
        "Execution Failed",
    )

    assert (
        context.failed
        is True
    )

    assert (
        context.reason
        == "Execution Failed"
    )