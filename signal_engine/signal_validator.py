"""
=================================================
Project Phoenix
Signal Validator
M34
=================================================
"""

from __future__ import annotations

from signal_engine.signal_context import (
    SignalContext,
)


class SignalValidator:
    """
    Validates SignalContext before and
    after signal generation.
    """

    def validate(
        self,
        context: SignalContext,
    ) -> bool:
        """
        Validate required data.
        """

        if not context.symbol:
            context.mark_failed(
                "Symbol is missing."
            )
            return False

        if not context.timeframe:
            context.mark_failed(
                "Timeframe is missing."
            )
            return False

        if not context.indicators:
            context.mark_failed(
                "Indicators are missing."
            )
            return False

        if not context.patterns:
            context.mark_failed(
                "Patterns are missing."
            )
            return False

        return True