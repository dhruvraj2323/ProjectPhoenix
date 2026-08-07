"""
=================================================
Project Phoenix
Live Trade Validator
M59.1.3
=================================================
"""

from __future__ import annotations

from live_execution.trade_context import (
    TradeContext,
)


class TradeValidator:
    """
    Validates trade requests before
    submitting them to MT5.
    """

    def validate(
        self,
        context: TradeContext,
    ) -> bool:
        """
        Validate trade context.
        """

        if not context.symbol:

            context.fail(
                "Symbol is required."
            )

            return False

        if context.risk_result is None:

            context.fail(
                "Risk result missing."
            )

            return False

        if context.signal_result is None:

            context.fail(
                "Signal result missing."
            )

            return False

        if context.strategy_result is None:

            context.fail(
                "Strategy result missing."
            )

            return False

        if context.ai_result is None:

            context.fail(
                "AI result missing."
            )

            return False

        return True