"""
=================================================
Project Phoenix
Test Portfolio Models
M35
=================================================
"""

from portfolio_engine.portfolio_models import (
    PortfolioSnapshot,
    PortfolioStatistics,
    PortfolioStatus,
    Position,
)


def test_portfolio_models():

    position = Position(
        symbol="XAUUSD",
        side="BUY",
        volume=0.10,
        entry_price=3300.0,
        current_price=3310.0,
        profit_loss=10.0,
    )

    statistics = PortfolioStatistics()

    snapshot = PortfolioSnapshot(
        account_id="ACC-001",
        balance=10000.0,
        equity=10010.0,
        margin=500.0,
        free_margin=9510.0,
        status=PortfolioStatus.COMPLETED,
    )

    snapshot.positions.append(position)

    assert snapshot.account_id == "ACC-001"
    assert snapshot.balance == 10000.0
    assert snapshot.positions[0].symbol == "XAUUSD"
    assert statistics.total_positions == 0
    assert snapshot.status == PortfolioStatus.COMPLETED