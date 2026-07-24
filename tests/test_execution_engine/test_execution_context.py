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
        signal="BUY",
        quantity=1.0,
        price=3350.50,
    )

    assert context.execution_id == "EXEC-001"

    assert context.symbol == "XAUUSD"

    assert context.signal == "BUY"

    assert context.quantity == 1.0

    assert context.price == 3350.50

    assert context.order is None

    assert context.completed is False

    assert context.failed is False

    assert context.reason == ""

    assert context.metadata == {}