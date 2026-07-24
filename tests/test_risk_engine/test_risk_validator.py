"""
=================================================
Project Phoenix
Test Risk Validator
M36
=================================================
"""

from risk_engine.risk_context import RiskContext
from risk_engine.risk_processor import RiskProcessor
from risk_engine.risk_validator import RiskValidator
from risk_engine.risk_models import RiskDecision


def test_risk_validator():

    processor = RiskProcessor()

    validator = RiskValidator()

    context = RiskContext(
        engine_id="RISK-001",
        account_id="ACC-001",
        balance=10000.0,
        equity=9950.0,
        free_margin=9900.0,
    )

    processor.process(
        context,
    )

    result = validator.validate(
        context,
    )

    assert result is True

    assert context.completed is True

    assert context.failed is False

    assert (
        context.risk_result.decision
        == RiskDecision.APPROVED
    )

    assert (
        context.risk_result.reason
        == "Risk Accepted"
    )