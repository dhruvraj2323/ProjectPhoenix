"""
=================================================
Project Phoenix
Test Paper Order Manager
M24
=================================================
"""

from paper_trading.paper_order_manager import (
    PaperOrderManager,
)


def test_paper_order_manager():

    manager = PaperOrderManager()

    order = manager.create_order(

        strategy_id="S01",

        symbol="XAUUSD",

        side="BUY",

        quantity=1.0,

        entry_price=3350.0,

        stop_loss=3340.0,

        take_profit=3370.0,

        risk_percent=1.0,

    )

    positions = manager.get_positions()

    assert order.symbol == "XAUUSD"

    assert order.side == "BUY"

    assert order.quantity == 1.0

    assert len(positions) == 1

    assert positions[0].ticket == 1

    assert positions[0].strategy_id == "S01"

    assert positions[0].side == "BUY"