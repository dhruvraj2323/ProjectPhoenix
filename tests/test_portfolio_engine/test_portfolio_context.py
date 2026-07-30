"""
=================================================
Project Phoenix
Test Portfolio Context
M35
=================================================
"""

from portfolio_engine.portfolio_context import (
    PortfolioContext,
)


def test_portfolio_context():

    context = PortfolioContext(

        portfolio_id="PF-001",

        account_id="ACC-001",

    )

    assert context.portfolio_id == "PF-001"

    assert context.account_id == "ACC-001"

    assert context.positions == []

    assert context.summary.balance == 10000.0

    assert context.metadata == {}

    assert context.approved is False

    assert context.completed is False

    assert context.failed is False

    assert context.decision == ""

    assert context.reason == ""

    context.approve(
        decision="PORTFOLIO_APPROVED",
        reason="Portfolio Accepted",
    )

    assert context.approved is True

    assert context.completed is True

    assert context.failed is False

    assert context.decision == "PORTFOLIO_APPROVED"

    assert context.reason == "Portfolio Accepted"

    context.reject(
        decision="PORTFOLIO_VALIDATION_FAILED",
        reason="Portfolio validation failed.",
    )

    assert context.approved is False

    assert context.completed is True

    assert context.failed is True

    assert context.decision == "PORTFOLIO_VALIDATION_FAILED"

    assert context.reason == "Portfolio validation failed."

    context.reset()

    assert context.approved is False

    assert context.completed is False

    assert context.failed is False

    assert context.decision == ""

    assert context.reason == ""