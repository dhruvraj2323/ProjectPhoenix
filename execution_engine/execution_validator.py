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
    Validates execution context.
    """

    def validate(
        self,
        context: ExecutionContext,
    ) -> bool:

        if not context.symbol:

            context.failed = True

            context.reason = "Missing symbol"

            return False

        if context.signal not in (
            "BUY",
            "SELL",
        ):

            context.failed = True

            context.reason = "Invalid signal"

            return False

        if context.quantity <= 0:

            context.failed = True

            context.reason = "Invalid quantity"

            return False

        if context.price <= 0:

            context.failed = True

            context.reason = "Invalid price"

            return False

        return True