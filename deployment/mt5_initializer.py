"""
=================================================
Project Phoenix
MT5 Initializer
M58
=================================================
"""

from __future__ import annotations

from live_trading.mt5_connector import (
    MT5Connector,
)


class MT5Initializer:
    """
    Initializes MT5 connection
    for deployment.
    """

    def __init__(
        self,
    ) -> None:

        self.connector = (
            MT5Connector()
        )

    # --------------------------------------------------
    # Connect
    # --------------------------------------------------

    def connect(
        self,
    ) -> bool:
        """
        Connect to MT5.
        """

        return (
            self.connector.connect()
        )

    # --------------------------------------------------
    # Disconnect
    # --------------------------------------------------

    def disconnect(
        self,
    ) -> None:
        """
        Disconnect MT5.
        """

        self.connector.disconnect()