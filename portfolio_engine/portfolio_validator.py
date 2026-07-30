"""
=================================================
Project Phoenix
Portfolio Validator
M35
=================================================
"""

from __future__ import annotations

from portfolio_engine.portfolio_context import (
    PortfolioContext,
)


class PortfolioValidator:
    """
    Validates Portfolio Engine input.
    """

    def validate(
        self,
        context: PortfolioContext,
    ) -> bool:

        if not context.portfolio_id:

            context.reject(
                decision="PORTFOLIO_VALIDATION_FAILED",
                reason="Portfolio ID is missing.",
            )

            return False

        if not context.account_id:

            context.reject(
                decision="PORTFOLIO_VALIDATION_FAILED",
                reason="Account ID is missing.",
            )

            return False

        if context.summary.balance < 0:

            context.reject(
                decision="PORTFOLIO_VALIDATION_FAILED",
                reason="Invalid account balance.",
            )

            return False

        if context.summary.equity < 0:

            context.reject(
                decision="PORTFOLIO_VALIDATION_FAILED",
                reason="Invalid account equity.",
            )

            return False

        context.approve(
            decision="PORTFOLIO_APPROVED",
            reason="Portfolio Accepted",
        )

        return True