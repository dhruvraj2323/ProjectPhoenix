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

    context.approve(
        decision="RISK_APPROVED",
        reason="Risk Accepted",
    )

    logger.log_finish(
        context,
    )

    assert (
        context.metadata["completed"]
        is True
    )

    assert context.completed is True
    assert context.approved is True
    assert context.failed is False
    assert context.decision == "RISK_APPROVED"

    context.reject(
        decision="RISK_VALIDATION_FAILED",
        reason="Risk limit exceeded",
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

    assert context.completed is True
    assert context.approved is False
    assert context.failed is True
    assert (
        context.decision
        == "RISK_VALIDATION_FAILED"
    )
    assert (
        context.reason
        == "Risk limit exceeded"
    )


if __name__ == "__main__":
    test_risk_logger()