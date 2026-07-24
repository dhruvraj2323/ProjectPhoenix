"""
=================================================
Project Phoenix
Test Execution Manager
M37
=================================================
"""

from execution_engine.execution_context import (
    ExecutionContext,
)
from execution_engine.execution_manager import (
    ExecutionManager,
)


def test_execution_manager():

    manager = ExecutionManager()

    context = ExecutionContext(
        execution_id="EXEC-001",
        symbol="XAUUSD",
        signal="BUY",
        quantity=1.0,
        price=3350.50,
    )

    result = manager.execute(
        context,
    )

    assert result.completed is True

    assert result.failed is False

    assert result.order is not None

    assert result.execution_result.accepted is True

    assert result.execution_result.status == "READY"

    assert result.metadata["started"] is True

    assert result.metadata["finished"] is True