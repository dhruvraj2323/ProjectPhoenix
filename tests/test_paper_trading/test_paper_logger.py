"""
=================================================
Project Phoenix
Test Paper Trading Logger
M24
=================================================
"""

from paper_trading.paper_context import (
    PaperContext,
)

from paper_trading.paper_logger import (
    PaperLogger,
)


def test_paper_logger():

    logger = PaperLogger()

    context = PaperContext(

        paper_id="PAPER-001",

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
        "Paper trading validation failed.",
    )

    logger.log_failure(
        context,
    )

    assert True