"""
=================================================
Project Phoenix
Position Closer
M59.3.5
=================================================
"""

from __future__ import annotations

import MetaTrader5 as mt5


class PositionCloser:
    """
    Closes MT5 positions.
    """

    def close(
        self,
        ticket: int,
        symbol: str,
        volume: float,
        order_type: int,
        price: float,
    ):

        request = {

            "action": mt5.TRADE_ACTION_DEAL,

            "position": ticket,

            "symbol": symbol,

            "volume": volume,

            "type": order_type,

            "price": price,

            "deviation": 20,

            "type_time": mt5.ORDER_TIME_GTC,

            "type_filling": mt5.ORDER_FILLING_IOC,

        }

        return mt5.order_send(
            request,
        )