"""
=================================================
Project Phoenix
Test Strategy Logger
M38
=================================================
"""

from strategy.strategy_context import (
    StrategyContext,
)

from strategy.strategy_logger import (
    StrategyLogger,
)


def test_strategy_logger():

    logger = StrategyLogger()

    context = StrategyContext(
        engine_id="STRATEGY-001",
        symbol="XAUUSD",
        timeframe="M15",
    )

    logger.log_start(
        context,
    )

    context.complete()

    logger.log_finish(
        context,
    )

    context.fail(
        "Validation Failed",
    )

    logger.log_failure(
        context,
    )

    assert context.failed is True

    assert (
        context.reason
        == "Validation Failed"
    )