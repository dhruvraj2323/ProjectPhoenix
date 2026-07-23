"""
=================================================
Project Phoenix
Indicator Validator
M32
=================================================
"""

from __future__ import annotations

from indicator_engine.indicator_context import IndicatorContext


class IndicatorValidator:
    """
    Validates indicator calculation requests
    before execution.
    """

    def validate(
        self,
        context: IndicatorContext,
    ) -> bool:
        """
        Validate indicator context.
        """

        if context.symbol == "":
            return False

        if context.timeframe == "":
            return False

        if context.candles is None:
            return False

        if len(context.candles) == 0:
            return False

        return True

    # ---------------------------------------------------------

    def validate_indicator(
        self,
        indicator_name: str,
    ) -> bool:
        """
        Validate supported indicator.
        """

        supported = {
            "EMA",
            "SMA",
            "RSI",
            "ATR",
            "MACD",
            "BOLLINGER_BANDS",
            "VWAP",
            "SUPERTREND",
        }

        return indicator_name.upper() in supported