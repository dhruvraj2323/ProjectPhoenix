"""
=================================================
Project Phoenix
Test Risk Processor
M36
=================================================
"""

from risk_engine.risk_context import RiskContext
from risk_engine.risk_processor import RiskProcessor
from risk_engine.risk_models import RiskDecision


def test_risk_processor():

    processor = RiskProcessor()

    context = RiskContext(
        engine_id="RISK-001",
        account_id="ACC-001",
        balance=10000.0,
        equity=9900.0,
        free_margin=9500.0,
    )

    result = processor.process(
        context,
    )

    assert (
        result.risk_result.metrics.risk_percent
        > 0
    )

    assert (
        result.risk_result.metrics.position_size
        == 0.10
    )

    assert (
        result.risk_result.metrics.exposure
        == 500.0
    )

    assert (
        result.risk_result.metrics.margin_required
        == 100.0
    )

    assert (
        result.risk_result.metrics.drawdown
        == 1.0
    )

    assert (
        result.risk_result.decision
        == RiskDecision.APPROVED
    )

    assert (
        result.risk_result.reason
        == "Risk Calculated"
    )