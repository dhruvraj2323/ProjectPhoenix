"""
=================================================
Project Phoenix
Paper Trading Validator
M54
=================================================
"""

from __future__ import annotations

from paper_trading.paper_context import (
    PaperContext,
)


class PaperValidator:
    """
    Validates Paper Trading Context
    before execution.
    """

    def validate(
        self,
        context: PaperContext,
    ) -> bool:
        """
        Validate Paper Trading input.
        """

        if not context.paper_id:

            context.fail(
                "Paper ID is missing.",
            )

            return False

        if not context.account_id:

            context.fail(
                "Account ID is missing.",
            )

            return False

        if not context.symbol:

            context.fail(
                "Trading symbol is missing.",
            )

            return False

        if context.execution_result is None:

            context.fail(
                "Execution result not available.",
            )

            return False

        return True