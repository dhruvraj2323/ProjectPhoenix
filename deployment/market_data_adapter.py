"""
=================================================
Project Phoenix
Market Data Adapter
M58.12.5
=================================================
"""

from __future__ import annotations

from typing import Any


class MarketDataAdapter:
    """
    Converts MT5 structured candle data
    into standard Python dictionaries.
    """

    # --------------------------------------------------

    def normalize(
        self,
        candles: list[Any],
    ) -> list[dict]:
        """
        Normalize MT5 candle format.

        numpy.void
            ↓
        dict
        """

        normalized = []

        for candle in candles:

            if isinstance(
                candle,
                dict,
            ):

                normalized.append(candle)

                continue

            normalized.append(
                {
                    "time": int(candle["time"]),
                    "open": float(candle["open"]),
                    "high": float(candle["high"]),
                    "low": float(candle["low"]),
                    "close": float(candle["close"]),
                    "tick_volume": int(
                        candle["tick_volume"]
                    ),
                    "spread": int(
                        candle["spread"]
                    ),
                    "real_volume": int(
                        candle["real_volume"]
                    ),
                }
            )

        return normalized