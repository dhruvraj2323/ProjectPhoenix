"""
=================================================
Project Phoenix
Position Modifier
M59.3.6
=================================================
"""

from __future__ import annotations

import MetaTrader5 as mt5


class PositionModifier:
    """
    Modify Stop Loss and
    Take Profit of an
    existing MT5 position.
    """

    def modify(
        self,
        ticket: int,
        symbol: str,
        stop_loss: float,
        take_profit: float,
    ):

        request = {

            "action": mt5.TRADE_ACTION_SLTP,

            "position": ticket,

            "symbol": symbol,

            "sl": stop_loss,

            "tp": take_profit,

        }

        return mt5.order_send(
            request,
        )