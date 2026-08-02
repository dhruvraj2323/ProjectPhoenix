"""
=================================================
Project Phoenix
Paper Order Manager
M24
=================================================
"""

from __future__ import annotations

from paper_trading.paper_models import (
    PaperOrder,
    PaperPosition,
)


class PaperOrderManager:
    """
    Creates virtual paper orders
    and positions.
    """

    def __init__(self) -> None:

        self._next_ticket = 1

        self.positions: list[PaperPosition] = []

    def create_order(

        self,

        strategy_id: str,

        symbol: str,

        side: str,

        quantity: float,

        entry_price: float,

        stop_loss: float,

        take_profit: float,

        risk_percent: float,

    ) -> PaperOrder:

        order = PaperOrder(

            strategy_id=strategy_id,

            symbol=symbol,

            side=side,

            quantity=quantity,

            entry_price=entry_price,

            stop_loss=stop_loss,

            take_profit=take_profit,

            risk_percent=risk_percent,

        )

        position = PaperPosition(

            ticket=self._next_ticket,

            strategy_id=strategy_id,

            symbol=symbol,

            side=side,

            quantity=quantity,

            entry_price=entry_price,

            current_price=entry_price,

            stop_loss=stop_loss,

            take_profit=take_profit,

        )

        self.positions.append(position)

        self._next_ticket += 1

        return order

    def get_positions(

        self,

    ) -> list[PaperPosition]:

        return self.positions