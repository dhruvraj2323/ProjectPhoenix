"""
=================================================
Project Phoenix
Test Risk Models
M36
=================================================
"""

from risk_engine.risk_models import (
    RiskDecision,
    RiskMetrics,
    RiskResult,
)


def test_risk_models():

    metrics = RiskMetrics(
        risk_percent=1.0,
        position_size=0.10,
        exposure=500.0,
        margin_required=100.0,
        drawdown=2.5,
    )

    result = RiskResult(
        decision=RiskDecision.APPROVED,
        reason="Risk Accepted",
        metrics=metrics,
    )

    assert result.decision == RiskDecision.APPROVED

    assert result.metrics.risk_percent == 1.0

    assert result.metrics.position_size == 0.10

    assert result.metrics.exposure == 500.0

    assert result.metrics.margin_required == 100.0

    assert result.metrics.drawdown == 2.5

    assert result.reason == "Risk Accepted"

    assert isinstance(
        result.metadata,
        dict,
    )