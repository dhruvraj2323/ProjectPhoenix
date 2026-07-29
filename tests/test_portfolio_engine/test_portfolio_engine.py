"""
=================================================
Project Phoenix
Test Portfolio Engine
M35
=================================================
"""

from portfolio_engine.portfolio_context import (
    PortfolioContext,
)

from portfolio_engine.portfolio_engine import (
    PortfolioEngine,
)

from portfolio_engine.portfolio_models import (
    PortfolioPosition,
)


def test_portfolio_engine():

    engine = PortfolioEngine()

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

            entry_price=3350,

            stop_loss=3340,

            take_profit=3370,

            current_price=3355,

            unrealized_pnl=50,

            realized_pnl=100,

        )

    )

    output = engine.run(
        context,
    )

    assert output.completed is True

    assert output.failed is False

    assert output.summary.total_trades == 1

    assert output.summary.equity == 10050

    assert output.summary.realized_pnl == 100

    assert output.summary.floating_pnl == 50