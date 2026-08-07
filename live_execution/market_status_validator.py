"""
=================================================
Project Phoenix
Market Status Validator
M59.4.2
=================================================
"""

from __future__ import annotations

import MetaTrader5 as mt5


class MarketStatusValidator:
    """
    Validates that a symbol is
    available and tradable.
    """

    def validate(
        self,
        symbol: str,
    ) -> bool:

        info = mt5.symbol_info(
            symbol,
        )

        if info is None:

            raise RuntimeError(
                f"Unknown symbol: {symbol}"
            )

        if not info.visible:

            if not mt5.symbol_select(
                symbol,
                True,
            ):

                raise RuntimeError(
                    f"Unable to select symbol: {symbol}"
                )

        if not info.trade_mode:

            raise RuntimeError(
                f"Trading disabled for {symbol}"
            )

        return True