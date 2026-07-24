"""
=================================================
Project Phoenix
Test Execution Processor
M37
=================================================
"""

from execution_engine.execution_context import (
    ExecutionContext,
)
from execution_engine.execution_processor import (
    ExecutionProcessor,
)


def test_execution_processor():

    processor = ExecutionProcessor()

    context = ExecutionContext(
        execution_id="EXEC-001",
        symbol="XAUUSD",
        signal="BUY",
        quantity=1.0,
        price=3350.50,
    )

    result = processor.process(
        context,
    )

    assert result.order is not None

    assert result.order.symbol == "XAUUSD"

    assert result.order.side == "BUY"

    assert result.order.quantity == 1.0

    assert result.execution_result.accepted is True

    assert result.execution_result.status == "READY"

    assert result.execution_result.order_id == "EXEC-001"

    assert result.execution_result.executed_price == 3350.50

    assert result.completed is True