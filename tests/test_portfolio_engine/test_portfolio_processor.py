"""
=================================================
Project Phoenix
Test Portfolio Processor
M35
=================================================
"""

from portfolio_engine.portfolio_context import (
    PortfolioContext,
)

from portfolio_engine.portfolio_models import (
    Position,
)

from portfolio_engine.portfolio_processor import (
    PortfolioProcessor,
)


def test_portfolio_processor():

    processor = PortfolioProcessor()

    context = PortfolioContext(
        engine_id="PORTFOLIO-001",
        account_id="ACC-001",
        balance=10000.0,
        margin=500.0,
    )

    context.add_position(

        Position(
            symbol="XAUUSD",
            side="BUY",
            volume=0.10,
            entry_price=3300.0,
            current_price=3310.0,
            profit_loss=100.0,
        )

    )

    result = processor.process(context)

    assert result.completed is True

    assert result.statistics.total_positions == 1

    assert result.statistics.winning_positions == 1

    assert result.statistics.losing_positions == 0

    assert result.equity == 10100.0

    assert result.free_margin == 9600.0