"""
=================================================
Project Phoenix
Test Execution Engine
M37
=================================================
"""

from execution_engine.execution_context import (
    ExecutionContext,
)
from execution_engine.execution_engine import (
    ExecutionEngine,
)


def test_execution_engine():

    engine = ExecutionEngine()

    context = ExecutionContext(
        execution_id="EXEC-001",
        symbol="XAUUSD",
        signal="BUY",
        quantity=1.0,
        price=3350.50,
    )

    result = engine.run(
        context,
    )

    assert result.completed is True

    assert result.failed is False

    assert result.order is not None

    assert result.execution_result.accepted is True

    assert result.execution_result.status == "READY"

    assert result.metadata["started"] is True

    assert result.metadata["finished"] is True