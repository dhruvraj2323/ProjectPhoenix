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

from portfolio_engine.portfolio_models import (
    Position,
)


def test_portfolio_context():

    context = PortfolioContext(
        engine_id="PORTFOLIO-001",
        account_id="ACC-001",
    )

    position = Position(
        symbol="XAUUSD",
        side="BUY",
        volume=0.10,
        entry_price=3300.0,
        current_price=3310.0,
        profit_loss=10.0,
    )

    context.add_position(position)

    assert len(context.positions) == 1

    context.remove_position("XAUUSD")

    assert len(context.positions) == 0

    context.metadata["test"] = True

    context.completed = True

    context.reset()

    assert context.completed is False
    assert context.failed is False
    assert context.reason == ""
    assert len(context.positions) == 0
    assert context.metadata == {}