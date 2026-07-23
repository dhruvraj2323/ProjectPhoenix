"""
=================================================
Project Phoenix
Pattern Validator
M33
=================================================
"""

from __future__ import annotations

from pattern_engine.pattern_context import (
    PatternContext,
)


class PatternValidator:
    """
    Validates Pattern Engine input/output.
    """

    def validate(
        self,
        context: PatternContext,
    ) -> bool:

        if not context.symbol:
            return False

        if not context.timeframe:
            return False

        if not isinstance(
            context.candles,
            list,
        ):
            return False

        return True