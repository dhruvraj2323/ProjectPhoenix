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

        timeframe="M15",

    )

    context.strategy_result = object()

    context.signal_result = object()

    context.risk_result = object()

    context.ai_result = object()

    assert (
        validator.validate(
            context,
        )
        is True
    )

    invalid = ExecutionContext(

        execution_id="EXEC-002",

        symbol="",

        timeframe="M15",

    )

    assert (
        validator.validate(
            invalid,
        )
        is False
    )

    assert invalid.failed is True

    assert (
        invalid.reason
        == "Symbol is missing."
    )