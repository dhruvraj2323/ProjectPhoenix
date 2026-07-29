"""
=================================================
Project Phoenix
Test Portfolio Manager
M35
=================================================
"""

from portfolio_engine.portfolio_context import (
    PortfolioContext,
)

from portfolio_engine.portfolio_manager import (
    PortfolioManager,
)

from portfolio_engine.portfolio_models import (
    PortfolioPosition,
)


def test_portfolio_manager():

    manager = PortfolioManager()

    context = PortfolioContext(

        portfolio_id="PF-001",

        account_id="ACC-001",

    )

    context.positions.append(

        PortfolioPosition(

            trade_id="TRD-001",

            symbol="XAUUSD",

            side="BUY",

            quantity=1.0,

            entry_price=3350.0,

            stop_loss=3340.0,

            take_profit=3370.0,

            current_price=3355.0,

            unrealized_pnl=50.0,

            realized_pnl=100.0,

        )

    )

    output = manager.update(
        context,
    )

    assert output.completed is True

    assert output.failed is False

    assert output.summary.total_trades == 1

    assert output.summary.equity == 10050.0

    assert output.summary.realized_pnl == 100.0

    assert output.summary.floating_pnl == 50.0