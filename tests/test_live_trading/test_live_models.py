"""
=================================================
Project Phoenix
Live Trading Models Test
=================================================
"""

from live_trading.live_models import (
    LiveOrder,
    LivePosition,
    LivePortfolio,
    LiveTradingStatus,
    LiveTradingResult,
)


def run_test():

    order = LiveOrder(
        ticket=1001,
        symbol="EURUSD",
        direction="BUY",
        volume=0.10,
        entry_price=1.1065,
    )

    position = LivePosition(
        ticket=1001,
        symbol="EURUSD",
        direction="BUY",
        volume=0.10,
        entry_price=1.1065,
        current_price=1.1072,
        profit=7.0,
    )

    portfolio = LivePortfolio(
        balance=10000.0,
        equity=10007.0,
        floating_profit=7.0,
        closed_profit=0.0,
    )

    status = LiveTradingStatus(
        running=True,
        account_balance=10000.0,
        total_positions=1,
    )

    result = LiveTradingResult(
        approved=True,
        reason="Live trading initialized successfully.",
        status=status,
    )

    print("===== Live Trading Models =====")

    print(f"Ticket          : {order.ticket}")
    print(f"Symbol          : {order.symbol}")
    print(f"Direction       : {order.direction}")
    print(f"Profit          : {position.profit}")
    print(f"Balance         : {portfolio.balance}")

    assert result.approved

    print()
    print("Live Trading Models Test Passed")


if __name__ == "__main__":

    run_test()