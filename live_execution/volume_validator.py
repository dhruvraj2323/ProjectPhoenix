"""
=================================================
Project Phoenix
Volume Validator
M59.4.3
=================================================
"""

from __future__ import annotations

import math

from live_execution.symbol_info import (
    SymbolInfo,
)


class VolumeValidator:
    """
    Validates trade volume
    against broker limits.
    """

    def __init__(
        self,
    ) -> None:

        self.symbol_info = SymbolInfo()

    def validate(
        self,
        symbol: str,
        volume: float,
    ) -> bool:

        minimum = self.symbol_info.volume_min(
            symbol,
        )

        maximum = self.symbol_info.volume_max(
            symbol,
        )

        step = self.symbol_info.volume_step(
            symbol,
        )

        if volume < minimum:

            raise RuntimeError(
                f"Volume below minimum ({minimum})."
            )

        if volume > maximum:

            raise RuntimeError(
                f"Volume above maximum ({maximum})."
            )

        units = volume / step

        if not math.isclose(
            units,
            round(units),
            rel_tol=1e-9,
            abs_tol=1e-9,
        ):

            raise RuntimeError(
                f"Invalid volume step ({step})."
            )

        return True