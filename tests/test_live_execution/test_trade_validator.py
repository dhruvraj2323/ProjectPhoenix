"""
=================================================
Project Phoenix
Test Live Trade Validator
M59.1.3
=================================================
"""

from live_execution.trade_context import (
    TradeContext,
)

from live_execution.trade_validator import (
    TradeValidator,
)


def test_trade_validator():

    validator = TradeValidator()

    context = TradeContext(

        execution_id="EXEC-001",

        symbol="EURUSD",

        timeframe="M15",

    )

    assert (

        validator.validate(
            context
        )

        is False

    )

    assert (

        context.reason

        == "Risk result missing."

    )

    context.risk_result = object()

    context.signal_result = object()

    context.strategy_result = object()

    context.ai_result = object()

    assert (

        validator.validate(
            context
        )

        is True

    )