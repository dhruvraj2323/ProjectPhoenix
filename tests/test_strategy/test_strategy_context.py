"""
=================================================
Project Phoenix
Test Strategy Context
M38
=================================================
"""

from strategy.strategy_context import (
    StrategyContext,
)

from strategy.strategy_models import (
    StrategyStatus,
)


def test_strategy_context():

    context = StrategyContext(
        engine_id="STRATEGY-001",
        symbol="XAUUSD",
        timeframe="M15",
    )

    assert context.engine_id == "STRATEGY-001"

    assert context.symbol == "XAUUSD"

    assert context.timeframe == "M15"

    assert (
        context.strategy_result.status
        == StrategyStatus.CREATED
    )

    context.complete()

    assert context.completed is True

    assert context.failed is False

    context.fail(
        "Strategy validation failed",
    )

    assert context.failed is True

    assert (
        context.reason
        == "Strategy validation failed"
    )

    context.reset()

    assert context.completed is False

    assert context.failed is False

    assert context.reason == ""

    assert (
        context.strategy_result.status
        == StrategyStatus.CREATED
    )