"""
=================================================
Project Phoenix
Signal Processor
M34
=================================================
"""

from __future__ import annotations

from signal_engine.signal_context import (
    SignalContext,
)


class SignalProcessor:
    """
    Processes indicators and patterns
    to generate trading signals.
    """

    def process(
        self,
        context: SignalContext,
    ) -> SignalContext:
        """
        Generate signals from available
        indicators and candlestick patterns.
        """

        sma = context.indicators.get(
            "SMA",
            0.0,
        )

        ema = context.indicators.get(
            "EMA",
            0.0,
        )

        has_doji = any(
            pattern.get("name") == "DOJI"
            for pattern in context.patterns
        )

        if ema > sma and has_doji:

            context.add_signal(
                {
                    "direction": "BUY",
                    "strength": "STRONG",
                    "reason": "EMA above SMA with DOJI confirmation",
                }
            )

        elif ema < sma and has_doji:

            context.add_signal(
                {
                    "direction": "SELL",
                    "strength": "STRONG",
                    "reason": "EMA below SMA with DOJI confirmation",
                }
            )

        else:

            context.add_signal(
                {
                    "direction": "NEUTRAL",
                    "strength": "WEAK",
                    "reason": "No confirmed setup",
                }
            )

        return context