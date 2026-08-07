"""
=================================================
Project Phoenix
Price Validator
M59.4.4
=================================================
"""

from __future__ import annotations

from live_execution.symbol_info import (
    SymbolInfo,
)


class PriceValidator:
    """
    Validates order prices
    using broker precision.
    """

    def __init__(
        self,
    ) -> None:

        self.symbol_info = SymbolInfo()

    def validate(
        self,
        symbol: str,
        price: float,
        stop_loss: float,
        take_profit: float,
    ) -> bool:

        digits = self.symbol_info.digits(
            symbol,
        )

        values = (
            price,
            stop_loss,
            take_profit,
        )

        for value in values:

            rounded = round(
                value,
                digits,
            )

            if abs(
                rounded - value
            ) > 1e-10:

                raise RuntimeError(
                    "Invalid price precision."
                )

        return True