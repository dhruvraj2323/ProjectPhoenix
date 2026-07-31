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
        """
        Detect candlestick patterns.

        M50.X.1
        Enhanced Doji Detection
        """

        DOJI_THRESHOLD = 0.10

        for index, candle in enumerate(context.candles):

            open_price = candle.get("open", 0.0)
            close_price = candle.get("close", 0.0)
            high = candle.get("high", 0.0)
            low = candle.get("low", 0.0)

            candle_range = high - low

            if candle_range <= 0:

                continue

            body = abs(close_price - open_price)

            body_ratio = body / candle_range

            if body_ratio <= DOJI_THRESHOLD:

                strength = round(
                    1.0 - (body_ratio / DOJI_THRESHOLD),
                    3,
                )

                context.add_pattern(
                    {
                        "name": "DOJI",
                        "index": index,
                        "strength": strength,
                        "body_ratio": round(body_ratio, 5),
                    }
                )

        return context