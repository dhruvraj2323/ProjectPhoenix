"""
=================================================
Project Phoenix
Paper Trading Validator
M24
=================================================
"""

from __future__ import annotations

from paper_trading.paper_context import (
    PaperContext,
)


class PaperValidator:
    """
    Validates Paper Trading input.
    """

    def validate(
        self,
        context: PaperContext,
    ) -> bool:

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

        if context.portfolio.balance < 0:

            context.fail(
                "Invalid virtual balance.",
            )

            return False

        if context.execution_result is None:

            context.fail(
                "Execution result not available.",
            )

            return False

        return True