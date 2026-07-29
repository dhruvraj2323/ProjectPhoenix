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
    PortfolioPosition,
)

from portfolio_engine.portfolio_processor import (
    PortfolioProcessor,
)


def test_portfolio_processor():

    processor = PortfolioProcessor()

    context = PortfolioContext(

        portfolio_id="PF-001",

        account_id="ACC-001",

    )

    context.positions.append(

        PortfolioPosition(

            trade_id="T1",

            symbol="XAUUSD",

            side="BUY",

            quantity=1.0,

            entry_price=3350,

            stop_loss=3340,

            take_profit=3370,

            current_price=3355,

            unrealized_pnl=50,

            realized_pnl=0,

        )

    )

    context.positions.append(

        PortfolioPosition(

            trade_id="T2",

            symbol="EURUSD",

            side="SELL",

            quantity=1.0,

            entry_price=1.1700,

            stop_loss=1.1750,

            take_profit=1.1600,

            current_price=1.1680,

            unrealized_pnl=0,

            realized_pnl=100,

        )

    )

    output = processor.process(
        context,
    )

    assert output.summary.total_trades == 2

    assert output.summary.floating_pnl == 50

    assert output.summary.realized_pnl == 100

    assert output.summary.equity == 10050

    assert output.summary.free_margin == 10050

    assert output.summary.winning_trades == 1

    assert output.summary.losing_trades == 0

    assert output.summary.win_rate == 50.0