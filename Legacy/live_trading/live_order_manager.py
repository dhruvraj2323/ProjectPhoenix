"""
=================================================
Project Phoenix
Live Order Manager
=================================================

Handles live order execution through broker interface.
"""

from broker.broker_factory import BrokerFactory
from live_trading.live_models import (
    LiveOrder,
    LivePosition,
)


class LiveOrderManager:
    """
    Executes live broker orders.
    """

    def __init__(self):

        self.broker = BrokerFactory.create("MT5")
        self.next_ticket = 1001
        self.positions = []

    def buy(self, symbol: str, volume: float, price: float):

        self.broker.connect()

        order = LiveOrder(
            ticket=self.next_ticket,
            symbol=symbol,
            direction="BUY",
            volume=volume,
            entry_price=price,
        )

        position = LivePosition(
            ticket=self.next_ticket,
            symbol=symbol,
            direction="BUY",
            volume=volume,
            entry_price=price,
            current_price=price,
            profit=0.0,
        )

        self.positions.append(position)

        self.next_ticket += 1

        return order

    def sell(self, symbol: str, volume: float, price: float):

        self.broker.connect()

        order = LiveOrder(
            ticket=self.next_ticket,
            symbol=symbol,
            direction="SELL",
            volume=volume,
            entry_price=price,
        )

        position = LivePosition(
            ticket=self.next_ticket,
            symbol=symbol,
            direction="SELL",
            volume=volume,
            entry_price=price,
            current_price=price,
            profit=0.0,
        )

        self.positions.append(position)

        self.next_ticket += 1

        return order

    def get_positions(self):

        return self.positions