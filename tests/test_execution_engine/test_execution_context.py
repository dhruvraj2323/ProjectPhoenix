"""
=================================================
Project Phoenix
Test Execution Context
M37
=================================================
"""

from execution_engine.execution_context import (
    ExecutionContext,
)


def test_execution_context():

    context = ExecutionContext(

        execution_id="EXEC-001",

        symbol="XAUUSD",

        timeframe="M15",

    )

    assert context.execution_id == "EXEC-001"

    assert context.symbol == "XAUUSD"

    assert context.timeframe == "M15"

    assert context.order is None

    assert context.completed is False

    assert context.failed is False

    assert context.reason == ""

    assert context.metadata == {}

    context.complete()

    assert context.completed is True

    assert context.failed is False

    context.fail(
        "Execution Failed",
    )

    assert context.failed is True

    assert (
        context.reason
        == "Execution Failed"
    )

    context.reset()

    assert context.completed is False

    assert context.failed is False

    assert context.reason == ""

    assert context.order is None