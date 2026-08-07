"""
=================================================
Project Phoenix
Symbol Information
M59.3.9
=================================================
"""

from __future__ import annotations

import MetaTrader5 as mt5


class SymbolInfo:
    """
    Provides MT5 symbol information.
    """

    def get(
        self,
        symbol: str,
    ):

        return mt5.symbol_info(
            symbol,
        )

    def digits(
        self,
        symbol: str,
    ) -> int:

        info = self.get(
            symbol,
        )

        if info is None:

            return 0

        return int(info.digits)

    def point(
        self,
        symbol: str,
    ) -> float:

        info = self.get(
            symbol,
        )

        if info is None:

            return 0.0

        return float(info.point)

    def spread(
        self,
        symbol: str,
    ) -> int:

        info = self.get(
            symbol,
        )

        if info is None:

            return 0

        return int(info.spread)

    def volume_min(
        self,
        symbol: str,
    ) -> float:

        info = self.get(
            symbol,
        )

        if info is None:

            return 0.0

        return float(info.volume_min)

    def volume_max(
        self,
        symbol: str,
    ) -> float:

        info = self.get(
            symbol,
        )

        if info is None:

            return 0.0

        return float(info.volume_max)

    def volume_step(
        self,
        symbol: str,
    ) -> float:

        info = self.get(
            symbol,
        )

        if info is None:

            return 0.0

        return float(info.volume_step)