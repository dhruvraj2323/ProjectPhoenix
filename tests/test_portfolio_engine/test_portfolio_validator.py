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

    assert context.approved is True

    assert context.completed is True

    assert context.failed is False

    assert (
        context.decision
        == "PORTFOLIO_APPROVED"
    )

    assert (
        context.reason
        == "Portfolio Accepted"
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

    assert invalid.approved is False

    assert invalid.completed is True

    assert invalid.failed is True

    assert (
        invalid.decision
        == "PORTFOLIO_VALIDATION_FAILED"
    )

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

    assert invalid.approved is False

    assert invalid.completed is True

    assert invalid.failed is True

    assert (
        invalid.decision
        == "PORTFOLIO_VALIDATION_FAILED"
    )

    assert (
        invalid.reason
        == "Invalid account balance."
    )