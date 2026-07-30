"""
=================================================
Project Phoenix
Test Risk Context
M36
=================================================
"""

from risk_engine.risk_context import (
    RiskContext,
)


def test_risk_context():

    context = RiskContext(
        engine_id="RISK-001",
        account_id="ACC-001",
        balance=10000.0,
        equity=9800.0,
        free_margin=9500.0,
    )

    assert context.account_id == "ACC-001"
    assert context.balance == 10000.0
    assert context.equity == 9800.0
    assert context.free_margin == 9500.0

    context.set_metadata(
        "broker",
        "Paper",
    )

    assert (
        context.get_metadata("broker")
        == "Paper"
    )

    context.approve(
        decision="RISK_APPROVED",
        reason="Risk Accepted",
    )

    assert context.completed is True
    assert context.approved is True
    assert context.failed is False
    assert context.decision == "RISK_APPROVED"
    assert context.reason == "Risk Accepted"

    context.reset()

    assert context.completed is False
    assert context.approved is False
    assert context.failed is False
    assert context.decision == ""
    assert context.reason == ""

    context.reject(
        decision="RISK_VALIDATION_FAILED",
        reason="Maximum risk exceeded.",
    )

    assert context.completed is True
    assert context.approved is False
    assert context.failed is True
    assert context.decision == "RISK_VALIDATION_FAILED"
    assert context.reason == "Maximum risk exceeded."


if __name__ == "__main__":
    test_risk_context()