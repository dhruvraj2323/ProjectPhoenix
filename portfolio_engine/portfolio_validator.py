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
    Validates PortfolioContext before processing.
    """

    def validate(
        self,
        context: PortfolioContext,
    ) -> bool:

        if not context.engine_id:

            context.failed = True
            context.reason = "Missing engine ID"

            return False

        if not context.account_id:

            context.failed = True
            context.reason = "Missing account ID"

            return False

        if context.balance < 0:

            context.failed = True
            context.reason = "Invalid balance"

            return False

        if context.margin < 0:

            context.failed = True
            context.reason = "Invalid margin"

            return False

        return True