"""
=================================================
Project Phoenix
Portfolio Logger
M35
=================================================
"""

from __future__ import annotations

import logging

from portfolio_engine.portfolio_context import (
    PortfolioContext,
)


class PortfolioLogger:
    """
    Portfolio Engine logger.
    """

    def __init__(self) -> None:

        self.logger = logging.getLogger(
            "PortfolioEngine"
        )

    def log_start(
        self,
        context: PortfolioContext,
    ) -> None:

        self.logger.info(

            "Portfolio Engine Started | "
            "Account=%s",

            context.account_id,

        )

    def log_success(
        self,
        context: PortfolioContext,
    ) -> None:

        self.logger.info(

            "Portfolio Engine Completed | "
            "Positions=%d",

            len(context.positions),

        )

    def log_failure(
        self,
        context: PortfolioContext,
    ) -> None:

        self.logger.error(

            "Portfolio Engine Failed | %s",

            context.reason,

        )