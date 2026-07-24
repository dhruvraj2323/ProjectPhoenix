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
        equity=10150.0,
        free_margin=9600.0,
    )

    assert context.engine_id == "RISK-001"

    assert context.account_id == "ACC-001"

    assert context.balance == 10000.0

    assert context.equity == 10150.0

    assert context.free_margin == 9600.0

    context.complete()

    assert context.completed is True

    assert context.failed is False

    context.fail(
        "Margin exceeded",
    )

    assert context.failed is True

    assert context.completed is False

    assert context.reason == "Margin exceeded"