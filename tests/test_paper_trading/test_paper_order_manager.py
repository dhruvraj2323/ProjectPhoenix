"""
=================================================
Project Phoenix
Paper Order Manager Test
=================================================
"""

from paper_trading.paper_order_manager import PaperOrderManager


def run_test():

    manager = PaperOrderManager()

    buy_order = manager.buy(
        symbol="EURUSD",
        volume=0.10,
        price=1.1065,
    )

    sell_order = manager.sell(
        symbol="GBPUSD",
        volume=0.20,
        price=1.2560,
    )

    positions = manager.get_positions()

    print("===== Paper Order Manager =====")

    print(f"BUY Ticket      : {buy_order.ticket}")
    print(f"SELL Ticket     : {sell_order.ticket}")
    print(f"Positions       : {len(positions)}")

    assert len(positions) == 2

    print()
    print("Paper Order Manager Test Passed")


if __name__ == "__main__":

    run_test()