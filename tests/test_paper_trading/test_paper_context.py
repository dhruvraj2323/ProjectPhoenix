"""
=================================================
Project Phoenix
Test Paper Trading Context
M24
=================================================
"""

from paper_trading.paper_context import (
    PaperContext,
)


def test_paper_context():

    context = PaperContext(

        paper_id="PAPER-001",

        account_id="ACC-001",

    )

    assert context.paper_id == "PAPER-001"

    assert context.account_id == "ACC-001"

    assert context.portfolio.balance == 10000.0

    assert context.positions == []

    assert context.metadata == {}

    assert context.completed is False

    assert context.failed is False

    assert context.reason == ""

    context.complete()

    assert context.completed is True

    assert context.failed is False

    context.fail(
        "Paper trading validation failed.",
    )

    assert context.completed is False

    assert context.failed is True

    assert context.reason == "Paper trading validation failed."