"""
=================================================
Project Phoenix
MT5 Order Sender
M59.3.1
=================================================
"""

from __future__ import annotations

import MetaTrader5 as mt5


class OrderSender:
    """
    Sends trade requests
    to MetaTrader 5.
    """

    def send(
        self,
        request: dict,
    ):

        return mt5.order_send(
            request,
        )