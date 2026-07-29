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

        portfolio_id="PF-001",

        account_id="ACC-001",

    )

    assert (
        validator.validate(
            context,
        )
        is True
    )

    invalid = PortfolioContext(

        portfolio_id="",

        account_id="ACC-001",

    )

    assert (
        validator.validate(
            invalid,
        )
        is False
    )

    assert invalid.failed is True

    assert (
        invalid.reason
        == "Portfolio ID is missing."
    )

    invalid = PortfolioContext(

        portfolio_id="PF-002",

        account_id="ACC-002",

    )

    invalid.summary.balance = -100

    assert (
        validator.validate(
            invalid,
        )
        is False
    )

    assert (
        invalid.reason
        == "Invalid account balance."
    )