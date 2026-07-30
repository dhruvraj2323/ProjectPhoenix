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

        # -------------------------------------------------
        # Indicator Values
        # -------------------------------------------------

        sma = context.indicators.get(
            "SMA_20"
        ) or 0.0

        ema = context.indicators.get(
            "EMA_20"
        ) or 0.0

        # -------------------------------------------------
        # Pattern Confirmation
        # -------------------------------------------------

        has_doji = any(
            pattern.get("name") == "DOJI"
            for pattern in context.patterns
        )

        # -------------------------------------------------
        # Signal Generation
        # -------------------------------------------------

        if ema > sma and has_doji:

            context.add_signal(
                {
                    "direction": "BUY",
                    "strength": "STRONG",
                    "reason": (
                        "EMA_20 above SMA_20 "
                        "with DOJI confirmation"
                    ),
                }
            )

        elif ema < sma and has_doji:

            context.add_signal(
                {
                    "direction": "SELL",
                    "strength": "STRONG",
                    "reason": (
                        "EMA_20 below SMA_20 "
                        "with DOJI confirmation"
                    ),
                }
            )

        else:

            context.add_signal(
                {
                    "direction": "NEUTRAL",
                    "strength": "WEAK",
                    "reason": (
                        "No confirmed setup"
                    ),
                }
            )

        return context