"""
=================================================
Project Phoenix
MT5 Demo Connector
M54
=================================================
"""

from __future__ import annotations

import MetaTrader5 as mt5


class MT5DemoConnector:
    """
    Wrapper around MT5 Demo Terminal.

    Used only for Paper Trading.
    """

    def __init__(
        self,
    ) -> None:

        self._connected = False

    # --------------------------------------------------
    # Connect
    # --------------------------------------------------

    def connect(
        self,
    ) -> bool:
        """
        Connect to MT5 terminal.
        """

        self._connected = mt5.initialize()

        return self._connected

    # --------------------------------------------------
    # Disconnect
    # --------------------------------------------------

    def disconnect(
        self,
    ) -> None:
        """
        Shutdown MT5 connection.
        """

        if self._connected:

            mt5.shutdown()

            self._connected = False

    # --------------------------------------------------
    # Connection Status
    # --------------------------------------------------

    def connected(
        self,
    ) -> bool:
        """
        Return current connection status.
        """

        return self._connected

    # --------------------------------------------------
    # Account Information
    # --------------------------------------------------

    def account_info(
        self,
    ):
        """
        Return MT5 account information.
        """

        if not self._connected:

            return None

        return mt5.account_info()

    # --------------------------------------------------
    # Current Market Price
    # --------------------------------------------------

    def market_price(
        self,
        symbol: str,
    ):
        """
        Return latest market tick.
        """

        if not self._connected:

            return None

        tick = mt5.symbol_info_tick(
            symbol,
        )

        if tick is None:

            return None

        return {
            "bid": tick.bid,
            "ask": tick.ask,
            "last": tick.last,
            "time": tick.time,
        }            