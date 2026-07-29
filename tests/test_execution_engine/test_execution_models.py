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
    ExecutionStatus,
)


def test_execution_models():

    order = ExecutionOrder(

        strategy_id="S01",

        symbol="XAUUSD",

        side="BUY",

        quantity=1.00,

        entry_price=3350.50,

        stop_loss=3342.00,

        take_profit=3368.00,

        risk_percent=1.0,

    )

    assert order.strategy_id == "S01"

    assert order.symbol == "XAUUSD"

    assert order.side == "BUY"

    assert order.quantity == 1.00

    assert order.entry_price == 3350.50

    assert order.stop_loss == 3342.00

    assert order.take_profit == 3368.00

    assert order.risk_percent == 1.0

    assert order.order_type == "MARKET"

    result = ExecutionResult()

    assert result.accepted is False

    assert (
        result.status
        == ExecutionStatus.PENDING
    )

    assert result.order_id == ""

    assert result.executed_price == 0.0

    assert result.reason == ""