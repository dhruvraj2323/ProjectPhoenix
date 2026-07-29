"""
=================================================
Project Phoenix
Test Portfolio Models
M35
=================================================
"""

from portfolio_engine.portfolio_models import (
    PortfolioPosition,
    PortfolioSummary,
    PositionStatus,
)


def test_portfolio_models():

    position = PortfolioPosition(

        trade_id="TRD-001",

        symbol="XAUUSD",

        side="BUY",

        quantity=1.0,

        entry_price=3350.0,

        stop_loss=3340.0,

        take_profit=3370.0,

        current_price=3352.0,

    )

    assert position.trade_id == "TRD-001"

    assert position.symbol == "XAUUSD"

    assert position.side == "BUY"

    assert position.quantity == 1.0

    assert position.entry_price == 3350.0

    assert position.stop_loss == 3340.0

    assert position.take_profit == 3370.0

    assert position.current_price == 3352.0

    assert position.unrealized_pnl == 0.0

    assert position.realized_pnl == 0.0

    assert position.status == PositionStatus.OPEN

    summary = PortfolioSummary()

    assert summary.balance == 10000.0

    assert summary.equity == 10000.0

    assert summary.free_margin == 10000.0

    assert summary.used_margin == 0.0

    assert summary.floating_pnl == 0.0

    assert summary.realized_pnl == 0.0

    assert summary.total_trades == 0

    assert summary.winning_trades == 0

    assert summary.losing_trades == 0

    assert summary.win_rate == 0.0