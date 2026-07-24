"""
=================================================
Project Phoenix
Test Execution Models
M37
=================================================
"""

from execution_engine.execution_models import (
    ExecutionOrder,
    ExecutionResult,
)


def test_execution_models():

    order = ExecutionOrder(
        symbol="XAUUSD",
        side="BUY",
        quantity=1.0,
        price=3350.50,
    )

    assert order.symbol == "XAUUSD"

    assert order.side == "BUY"

    assert order.quantity == 1.0

    assert order.price == 3350.50

    assert order.order_type == "MARKET"

    result = ExecutionResult()

    assert result.accepted is False

    assert result.status == "PENDING"

    assert result.order_id == ""

    assert result.executed_price == 0.0

    assert result.reason == ""