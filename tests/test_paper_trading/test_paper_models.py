"""
=================================================
Project Phoenix
Paper Trading Models Test
=================================================
"""

from paper_trading.paper_models import (
    PaperOrder,
    PaperPosition,
    PaperPortfolio,
    PaperTradingStatus,
    PaperTradingResult,
)


def run_test():

    order = PaperOrder(
        ticket=1,
        symbol="EURUSD",
        direction="BUY",
        volume=0.10,
        entry_price=1.1065,
    )

    position = PaperPosition(
        ticket=1,
        symbol="EURUSD",
        direction="BUY",
        volume=0.10,
        entry_price=1.1065,
        current_price=1.1075,
        profit=10.0,
    )

    portfolio = PaperPortfolio(
        balance=10000.0,
        equity=10010.0,
        floating_profit=10.0,
        closed_profit=0.0,
    )

    status = PaperTradingStatus(
        running=True,
        virtual_balance=10000.0,
        total_positions=1,
    )

    result = PaperTradingResult(
        approved=True,
        reason="Paper trading initialized successfully.",
        status=status,
    )

    print("===== Paper Trading Models =====")

    print(f"Ticket          : {order.ticket}")
    print(f"Symbol          : {order.symbol}")
    print(f"Direction       : {order.direction}")
    print(f"Profit          : {position.profit}")
    print(f"Balance         : {portfolio.balance}")

    assert result.approved

    print()
    print("Paper Trading Models Test Passed")


if __name__ == "__main__":

    run_test()