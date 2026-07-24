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


def test_execution_logger():

    logger = ExecutionLogger()

    context = ExecutionContext(
        execution_id="EXEC-001",
        symbol="XAUUSD",
        signal="BUY",
        quantity=1.0,
        price=3350.50,
    )

    logger.log_start(
        context,
    )

    assert context.metadata["started"] is True

    logger.log_finish(
        context,
    )

    assert context.metadata["finished"] is True

    logger.log_failure(
        context,
    )

    assert context.metadata["failed"] is True