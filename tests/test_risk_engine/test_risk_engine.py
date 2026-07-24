"""
=================================================
Project Phoenix
Test Risk Engine
M36
=================================================
"""

from risk_engine.risk_context import RiskContext
from risk_engine.risk_engine import RiskEngine


def test_risk_engine():

    engine = RiskEngine()

    context = RiskContext(
        engine_id="RISK-001",
        account_id="ACC-001",
        balance=10000.0,
        equity=9950.0,
        free_margin=9900.0,
    )

    result = engine.run(
        context,
    )

    assert result.completed is True

    assert result.failed is False

    assert result.metadata["started"] is True

    assert result.metadata["completed"] is True

    assert (
        result.risk_result.reason
        == "Risk Accepted"
    )