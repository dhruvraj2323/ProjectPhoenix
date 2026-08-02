"""
=================================================
Project Phoenix
Live Trading Validator
M55
=================================================
"""

from __future__ import annotations

from live_trading.live_context import LiveContext


class LiveValidator:
    """
    Validates Live Trading
    execution context.
    """

    def validate(
        self,
        context: LiveContext,
    ) -> bool:
        """
        Validate runtime context.
        """

        if not context.symbol:

            context.fail(
                "Missing trading symbol.",
            )

            return False

        if not context.timeframe:

            context.fail(
                "Missing timeframe.",
            )

            return False

        if context.market_price <= 0:

            context.fail(
                "Invalid market price.",
            )

            return False

        return True