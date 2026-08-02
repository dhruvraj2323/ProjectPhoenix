"""
=================================================
Project Phoenix
Test Paper Trading Manager
M24
=================================================
"""

from paper_trading.paper_context import (
    PaperContext,
)

from paper_trading.paper_manager import (
    PaperTradingManager,
)


def test_paper_manager():

    manager = PaperTradingManager()

    context = PaperContext(

        paper_id="PAPER-001",

        account_id="ACC-001",

    )

    context.execution_result = object()

    output = manager.execute(
        context,
    )

    assert output.completed is True

    assert output.failed is False

    assert output.result.approved is True

    assert (
        output.result.status.running
        is True
    )