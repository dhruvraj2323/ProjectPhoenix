"""
=================================================
Project Phoenix
Live Order Manager Test
=================================================
"""

from live_trading.live_order_manager import LiveOrderManager


def run_test():

    manager = LiveOrderManager()

    buy = manager.buy(
        symbol="EURUSD",
        volume=0.10,
        price=1.1065,
    )

    sell = manager.sell(
        symbol="GBPUSD",
        volume=0.20,
        price=1.2560,
    )

    positions = manager.get_positions()

    print("===== Live Order Manager =====")

    print(f"BUY Ticket      : {buy.ticket}")
    print(f"SELL Ticket     : {sell.ticket}")
    print(f"Positions       : {len(positions)}")

    assert len(positions) == 2

    print()
    print("Live Order Manager Test Passed")


if __name__ == "__main__":

    run_test()