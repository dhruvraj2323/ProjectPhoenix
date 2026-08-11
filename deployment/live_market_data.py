"""
=================================================
Project Phoenix
Live Market Data
M58.12.1
=================================================
"""

from __future__ import annotations

from typing import Any

import MetaTrader5 as mt5

from live_trading.mt5_connector import (
    MT5Connector,
)


class LiveMarketData:
    """
    Downloads live market data
    from MetaTrader 5.
    """

    def __init__(
        self,
    ) -> None:

        self.connector = MT5Connector()

        self.timeframes = {
            "D1": mt5.TIMEFRAME_D1,
            "H4": mt5.TIMEFRAME_H4,
            "H1": mt5.TIMEFRAME_H1,
            "M15": mt5.TIMEFRAME_M15,
            "M5": mt5.TIMEFRAME_M5,
        }

    # --------------------------------------------------
    # Connect
    # --------------------------------------------------

    def connect(
        self,
    ) -> bool:

        return self.connector.connect()

    # --------------------------------------------------
    # Disconnect
    # --------------------------------------------------

    def disconnect(
        self,
    ) -> None:

        self.connector.disconnect()

    # --------------------------------------------------
    # Resolve Broker Symbol
    # --------------------------------------------------

    def resolve_symbol(
        self,
        symbol: str,
    ) -> str | None:
        """
        Automatically resolve broker-specific
        symbol names.

        Supports exact symbol matching first,
        followed by prefix matching.
        """

        symbols = mt5.symbols_get()

        if symbols is None:
            return None

        # Exact match
        for item in symbols:

            if item.name.upper() == symbol.upper():
                return item.name

        # Prefix match
        for item in symbols:

            if item.name.upper().startswith(
                symbol.upper()
            ):
                return item.name

        return None

    # --------------------------------------------------
    # Get Candles
    # --------------------------------------------------

    def get_candles(
        self,
        symbol: str,
        timeframe: str,
        bars: int = 500,
    ) -> list[dict[str, Any]]:

        resolved_symbol = self.resolve_symbol(
            symbol
        )

        if resolved_symbol is None:
            return []

        mt5_timeframe = self.timeframes[
            timeframe
        ]

        rates = mt5.copy_rates_from_pos(
            resolved_symbol,
            mt5_timeframe,
            0,
            bars,
        )

        if rates is None:
            return []

        return list(rates)

    # --------------------------------------------------
    # Multi Timeframe Data
    # --------------------------------------------------

    def get_multi_timeframe_data(
        self,
        symbol: str,
        bars: int = 500,
    ) -> dict[str, list[dict[str, Any]]]:

        market_data = {}

        for timeframe in self.timeframes:

            market_data[
                timeframe
            ] = self.get_candles(
                symbol,
                timeframe,
                bars,
            )

        return market_data