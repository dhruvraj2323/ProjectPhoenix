"""
=================================================
Project Phoenix
Test Execution Validator
M37
=================================================
"""

from execution_engine.execution_context import (
    ExecutionContext,
)
from execution_engine.execution_validator import (
    ExecutionValidator,
)


def test_execution_validator():

    validator = ExecutionValidator()

    context = ExecutionContext(
        execution_id="EXEC-001",
        symbol="XAUUSD",
        signal="BUY",
        quantity=1.0,
        price=3350.50,
    )

    assert validator.validate(
        context,
    ) is True

    bad_context = ExecutionContext(
        execution_id="EXEC-002",
        symbol="",
        signal="BUY",
        quantity=1.0,
        price=3350.50,
    )

    assert validator.validate(
        bad_context,
    ) is False

    assert bad_context.failed is True

    assert bad_context.reason == "Missing symbol"