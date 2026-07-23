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
        engine_id="PORTFOLIO-001",
        account_id="ACC-001",
    )

    logger.log_start(context)

    logger.log_success(context)

    context.failed = True

    context.reason = "Test Failure"

    logger.log_failure(context)

    assert context.failed is True

    assert context.reason == "Test Failure"