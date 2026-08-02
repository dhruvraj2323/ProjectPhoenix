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
    Validates Paper Trading input.
    """

    # --------------------------------------------------
    # Public Validation
    # --------------------------------------------------

    def validate(
        self,
        context: PaperContext,
    ) -> bool:
        """
        Validate PaperContext.
        """

        if not self._validate_identity(
            context,
        ):
            return False

        if not self._validate_market(
            context,
        ):
            return False

        if not self._validate_account(
            context,
        ):
            return False

        if not self._validate_execution(
            context,
        ):
            return False

        return True

    # --------------------------------------------------
    # Identity Validation
    # --------------------------------------------------

    def _validate_identity(
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

        return True

    # --------------------------------------------------
    # Market Validation
    # --------------------------------------------------

    def _validate_market(
        self,
        context: PaperContext,
    ) -> bool:

        if context.market_price <= 0.0:

            context.fail(
                "Invalid market price.",
            )

            return False

        if context.spread < 0.0:

            context.fail(
                "Invalid spread.",
            )

            return False

        return True

    # --------------------------------------------------
    # Account Validation
    # --------------------------------------------------

    def _validate_account(
        self,
        context: PaperContext,
    ) -> bool:

        if context.balance <= 0.0:

            context.fail(
                "Invalid account balance.",
            )

            return False

        if context.equity <= 0.0:

            context.fail(
                "Invalid account equity.",
            )

            return False

        if context.leverage <= 0.0:

            context.fail(
                "Invalid account leverage.",
            )

            return False

        return True

    # --------------------------------------------------
    # Execution Validation
    # --------------------------------------------------

    def _validate_execution(
        self,
        context: PaperContext,
    ) -> bool:

        if context.execution_result is None:

            context.fail(
                "Execution result is missing.",
            )

            return False

        return True        