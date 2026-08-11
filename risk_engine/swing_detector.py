"""
=================================================
Project Phoenix
Swing Detector
M59.7.5A
=================================================
"""

from __future__ import annotations


class SwingDetector:
    """
    Detects confirmed Swing Highs
    and Swing Lows from OHLC data.
    """

    def last_swing_high(
        self,
        candles: list[dict],
    ) -> float:

        if len(candles) < 3:

            return 0.0

        latest = 0.0

        for i in range(
            1,
            len(candles) - 1,
        ):

            previous = candles[i - 1]

            current = candles[i]

            next_candle = candles[i + 1]

            if (

                current["high"]
                > previous["high"]

                and

                current["high"]
                > next_candle["high"]

            ):

                latest = current["high"]

        return latest

    # --------------------------------------------------

    def last_swing_low(
        self,
        candles: list[dict],
    ) -> float:

        if len(candles) < 3:

            return 0.0

        latest = 0.0

        for i in range(
            1,
            len(candles) - 1,
        ):

            previous = candles[i - 1]

            current = candles[i]

            next_candle = candles[i + 1]

            if (

                current["low"]
                < previous["low"]

                and

                current["low"]
                < next_candle["low"]

            ):

                latest = current["low"]

        return latest