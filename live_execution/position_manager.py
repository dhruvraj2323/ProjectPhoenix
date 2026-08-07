"""
=================================================
Project Phoenix
Position Manager
M59.3.3
=================================================
"""

from __future__ import annotations

import MetaTrader5 as mt5


class PositionManager:
    """
    Provides access to MT5 positions.
    """

    def get_positions(
        self,
        symbol: str | None = None,
    ):

        if symbol is None:

            return mt5.positions_get()

        return mt5.positions_get(
            symbol=symbol,
        )

    def total_positions(
        self,
        symbol: str | None = None,
    ) -> int:

        positions = self.get_positions(
            symbol,
        )

        if positions is None:

            return 0

        return len(
            positions,
        )