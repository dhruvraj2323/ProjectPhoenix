"""
=================================================
Project Phoenix
Test Execution Logger
M37
=================================================
"""

from execution_engine.execution_context import (
    ExecutionContext,
)

from execution_engine.execution_logger import (
    ExecutionLogger,
)

from execution_engine.execution_models import (
    ExecutionOrder,
)


def test_execution_logger():

    logger = ExecutionLogger()

    context = ExecutionContext(

        execution_id="EXEC-001",

        symbol="XAUUSD",

        timeframe="M15",

    )

    logger.log_start(
        context,
    )

    context.order = ExecutionOrder(

        strategy_id="S01",

        symbol="XAUUSD",

        side="BUY",

        quantity=1.0,

        entry_price=3350,

        stop_loss=3340,

        take_profit=3370,

        risk_percent=1,

    )

    logger.log_order(
        context,
    )

    logger.log_finish(
        context,
    )

    context.fail(
        "Execution Failed",
    )

    logger.log_failure(
        context,
    )

    assert True