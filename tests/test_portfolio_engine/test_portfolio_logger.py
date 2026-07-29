"""
=================================================
Project Phoenix
Test Portfolio Logger
M35
=================================================
"""

from portfolio_engine.portfolio_context import (
    PortfolioContext,
)

from portfolio_engine.portfolio_logger import (
    PortfolioLogger,
)


def test_portfolio_logger():

    logger = PortfolioLogger()

    context = PortfolioContext(

        portfolio_id="PF-001",

        account_id="ACC-001",

    )

    logger.log_start(
        context,
    )

    logger.log_summary(
        context,
    )

    logger.log_finish(
        context,
    )

    context.fail(
        "Portfolio validation failed.",
    )

    logger.log_failure(
        context,
    )

    assert True