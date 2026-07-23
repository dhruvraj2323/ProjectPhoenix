"""
=================================================
Project Phoenix
Test Portfolio Validator
M35
=================================================
"""

from portfolio_engine.portfolio_context import (
    PortfolioContext,
)

from portfolio_engine.portfolio_validator import (
    PortfolioValidator,
)


def test_portfolio_validator():

    validator = PortfolioValidator()

    context = PortfolioContext(
        engine_id="PORTFOLIO-001",
        account_id="ACC-001",
        balance=10000.0,
        margin=500.0,
    )

    assert validator.validate(context) is True

    invalid = PortfolioContext(
        engine_id="",
        account_id="ACC-001",
    )

    assert validator.validate(invalid) is False

    assert invalid.failed is True

    assert invalid.reason == "Missing engine ID"