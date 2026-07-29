"""
=================================================
Project Phoenix
Paper Trading Engine
M24
=================================================
"""

from __future__ import annotations

from paper_trading.paper_context import PaperContext
from paper_trading.paper_logger import PaperLogger
from paper_trading.paper_portfolio import PaperPortfolioManager
from paper_trading.paper_validator import PaperValidator


class PaperTradingEngine:
    """
    Main Paper Trading Engine.
    """

    def __init__(self) -> None:

        self.validator = PaperValidator()

        self.portfolio = PaperPortfolioManager()

        self.logger = PaperLogger()

    def run(
        self,
        context: PaperContext,
    ) -> PaperContext:
        """
        Execute complete Paper Trading workflow.
        """

        self.logger.log_start(context)

        if not self.validator.validate(context):

            self.logger.log_failure(context)

            return context

        # Synchronize virtual portfolio into PaperContext
        context = self.portfolio.update_context(context)

        context.result.approved = True

        context.result.reason = (
            "Paper trading completed successfully."
        )

        context.result.status.running = True

        context.result.status.virtual_balance = (
            context.portfolio.balance
        )

        context.result.status.total_positions = (
            context.portfolio.total_positions
        )

        context.complete()

        self.logger.log_summary(context)

        self.logger.log_finish(context)

        return context