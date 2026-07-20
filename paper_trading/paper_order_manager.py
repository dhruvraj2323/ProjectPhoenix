"""
=================================================
Project Phoenix
Paper Order Manager
=================================================

Handles virtual order execution.
"""

from paper_trading.paper_models import (
    PaperOrder,
    PaperPosition,
)


class PaperOrderManager:
    """
    Executes virtual paper orders.
    """

    def __init__(self):

        self.next_ticket = 1
        self.positions = []

    def buy(self, symbol: str, volume: float, price: float):

        order = PaperOrder(
            ticket=self.next_ticket,
            symbol=symbol,
            direction="BUY",
            volume=volume,
            entry_price=price,
        )

        position = PaperPosition(
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

        order = PaperOrder(
            ticket=self.next_ticket,
            symbol=symbol,
            direction="SELL",
            volume=volume,
            entry_price=price,
        )

        position = PaperPosition(
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