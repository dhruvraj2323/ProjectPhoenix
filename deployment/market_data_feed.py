"""
=================================================
Project Phoenix
Market Data Feed
M58
=================================================
"""

from __future__ import annotations

from live_trading.mt5_connector import (
    MT5Connector,
)


class MarketDataFeed:
    """
    Retrieves live market data
    from MT5.
    """

    def __init__(
        self,
    ) -> None:

        self.connector = (
            MT5Connector()
        )

    # --------------------------------------------------
    # Fetch Timeframes
    # --------------------------------------------------

    def fetch(
        self,
    ) -> dict[str, object]:
        """
        Return market data for
        all deployment timeframes.
        """

        return {

            "D1": None,

            "H4": None,

            "H1": None,

            "M15": None,

            "M5": None,

        }