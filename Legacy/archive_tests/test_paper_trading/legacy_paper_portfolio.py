"""
=================================================
Project Phoenix
Test Paper Portfolio
M24
=================================================
"""

from paper_trading.paper_portfolio import (
    PaperPortfolioManager,
)


def test_paper_portfolio():

    manager = PaperPortfolioManager()

    portfolio = manager.portfolio()

    assert portfolio.balance == 10000.0

    assert portfolio.equity == 10000.0

    assert portfolio.floating_pnl == 0.0

    assert portfolio.realized_pnl == 0.0

    assert portfolio.total_positions == 0

    manager.update_floating_profit(125.50)

    portfolio = manager.portfolio()

    assert portfolio.floating_pnl == 125.50

    assert portfolio.equity == 10125.50

    manager.close_trade(50.0)

    portfolio = manager.portfolio()

    assert portfolio.balance == 10050.0

    assert portfolio.realized_pnl == 50.0

    assert portfolio.equity == 10175.50

    manager.add_position()

    manager.add_position()

    portfolio = manager.portfolio()

    assert portfolio.total_positions == 2

    manager.remove_position()

    portfolio = manager.portfolio()

    assert portfolio.total_positions == 1