"""
=================================================
Project Phoenix
Test Risk Logger
M36
=================================================
"""

from risk_engine.risk_context import RiskContext
from risk_engine.risk_logger import RiskLogger


def test_risk_logger():

    logger = RiskLogger()

    context = RiskContext(
        engine_id="RISK-001",
        account_id="ACC-001",
        balance=10000.0,
        equity=9950.0,
        free_margin=9800.0,
    )

    logger.log_start(
        context,
    )

    assert (
        context.metadata["started"]
        is True
    )

    logger.log_finish(
        context,
    )

    assert (
        context.metadata["completed"]
        is True
    )

    context.fail(
        "Risk limit exceeded",
    )

    logger.log_failure(
        context,
    )

    assert (
        context.metadata["failed"]
        is True
    )

    assert (
        context.metadata["reason"]
        == "Risk limit exceeded"
    )