"""
=================================================
Project Phoenix
Broker Models Test
=================================================
"""

from broker.broker_models import (
    BrokerAccount,
    BrokerOrder,
    BrokerPosition,
    BrokerBalance,
    BrokerSymbol,
    BrokerStatus,
    BrokerResult,
)


def run_test():

    account = BrokerAccount(
        account_id=10001,
        broker_name="MT5",
        balance=10000.0,
        equity=10125.5,
        margin=500.0,
        free_margin=9625.5,
    )

    order = BrokerOrder(
        ticket=1,
        symbol="EURUSD",
        order_type="BUY",
        volume=0.10,
        price=1.1050,
        status="OPEN",
    )

    position = BrokerPosition(
        ticket=1,
        symbol="EURUSD",
        direction="BUY",
        volume=0.10,
        open_price=1.1050,
        current_price=1.1075,
        profit=25.0,
    )

    balance = BrokerBalance(
        balance=10000.0,
        equity=10125.5,
        margin=500.0,
        free_margin=9625.5,
    )

    symbol = BrokerSymbol(
        symbol="EURUSD",
        digits=5,
        spread=12,
        trade_allowed=True,
    )

    status = BrokerStatus(
        connected=True,
        logged_in=True,
        broker_name="MT5",
    )

    result = BrokerResult(
        approved=True,
        reason="Broker connected successfully.",
        status=status,
    )

    print("===== Broker Models =====")

    print(f"Broker        : {account.broker_name}")
    print(f"Balance       : {account.balance}")
    print(f"Order         : {order.order_type}")
    print(f"Position P/L  : {position.profit}")
    print(f"Spread        : {symbol.spread}")
    print(f"Connected     : {status.connected}")

    assert result.approved

    print()
    print("Broker Models Test Passed")


if __name__ == "__main__":

    run_test()