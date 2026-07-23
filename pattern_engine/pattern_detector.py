"""
=================================================
Project Phoenix
Pattern Detector
M33
=================================================
"""

from __future__ import annotations

from pattern_engine.pattern_context import (
    PatternContext,
)


class PatternDetector:
    """
    Detects candlestick patterns.
    """

    def detect(
        self,
        context: PatternContext,
    ) -> PatternContext:

        for candle in context.candles:

            open_price = candle.get(
                "open",
                0,
            )

            close_price = candle.get(
                "close",
                0,
            )

            high = candle.get(
                "high",
                0,
            )

            low = candle.get(
                "low",
                0,
            )

            body = abs(
                close_price - open_price
            )

            candle_range = high - low

            if (
                candle_range > 0
                and body <= candle_range * 0.10
            ):

                context.add_pattern(
                    {
                        "name": "DOJI",
                        "strength": 1.0,
                    }
                )

        return context