"""
=================================================
Project Phoenix
Execution Validator
M37
=================================================
"""

from __future__ import annotations

from execution_engine.execution_context import (
    ExecutionContext,
)


class ExecutionValidator:
    """
    Validates execution request
    before trade execution.
    """

    def validate(
        self,
        context: ExecutionContext,
    ) -> bool:

        if not context.symbol:

            context.fail(
                "Symbol is missing.",
            )

            return False

        if context.strategy_result is None:

            context.fail(
                "Strategy result missing.",
            )

            return False

        if context.signal_result is None:

            context.fail(
                "Signal result missing.",
            )

            return False

        if context.risk_result is None:

            context.fail(
                "Risk result missing.",
            )

            return False

        if context.ai_result is None:

            context.fail(
                "AI decision missing.",
            )

            return False

        return True