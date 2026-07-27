"""
=================================================
Project Phoenix
Strategy Validator
M38
=================================================
"""

from __future__ import annotations

from strategy.strategy_context import (
    StrategyContext,
)


class StrategyValidator:
    """
    Validates Strategy Engine input
    before strategy execution.
    """

    def validate(
        self,
        context: StrategyContext,
    ) -> bool:
        """
        Validate required strategy inputs.
        """

        if not context.symbol:

            context.fail(
                "Symbol is missing.",
            )

            return False

        if not context.timeframe:

            context.fail(
                "Timeframe is missing.",
            )

            return False

        if not context.indicators:

            context.fail(
                "Indicators are missing.",
            )

            return False

        if not context.patterns:

            context.fail(
                "Patterns are missing.",
            )

            return False

        if not context.market_data:

            context.fail(
                "Market data is missing.",
            )

            return False

        return True