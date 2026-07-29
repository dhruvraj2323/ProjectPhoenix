"""
=================================================
Project Phoenix
Test Paper Trading Models
M24
=================================================
"""

from paper_trading.paper_models import (
    PaperOrder,
    PaperPosition,
    PaperPortfolio,
    PaperTradingStatus,
    PaperTradingResult,
    PaperPositionStatus,
)


def test_paper_models():

    order = PaperOrder(

        strategy_id="S01",

        symbol="XAUUSD",

        side="BUY",

        quantity=1.0,

        entry_price=3350.0,

        stop_loss=3340.0,

        take_profit=3370.0,

        risk_percent=1.0,

    )

    assert order.symbol == "XAUUSD"

    assert order.side == "BUY"

    assert order.quantity == 1.0

    position = PaperPosition(

        ticket=1,

        strategy_id="S01",

        symbol="XAUUSD",

        side="BUY",

        quantity=1.0,

        entry_price=3350.0,

        current_price=3355.0,

        stop_loss=3340.0,

        take_profit=3370.0,

        unrealized_pnl=50.0,

    )

    assert position.ticket == 1

    assert position.status == (
        PaperPositionStatus.OPEN
    )

    portfolio = PaperPortfolio()

    assert portfolio.balance == 10000.0

    assert portfolio.equity == 10000.0

    status = PaperTradingStatus()

    assert status.running is False

    result = PaperTradingResult()

    assert result.approved is False

    assert result.reason == ""