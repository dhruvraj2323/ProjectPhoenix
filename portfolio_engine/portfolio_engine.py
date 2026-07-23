"""
=================================================
Project Phoenix
Portfolio Engine
M35
=================================================
"""

from __future__ import annotations

from portfolio_engine.portfolio_context import (
    PortfolioContext,
)
from portfolio_engine.portfolio_logger import (
    PortfolioLogger,
)
from portfolio_engine.portfolio_processor import (
    PortfolioProcessor,
)
from portfolio_engine.portfolio_validator import (
    PortfolioValidator,
)


class PortfolioEngine:
    """
    Executes complete Portfolio pipeline.
    """

    def __init__(self) -> None:

        self.processor = PortfolioProcessor()

        self.validator = PortfolioValidator()

        self.logger = PortfolioLogger()

    def run(
        self,
        context: PortfolioContext,
    ) -> PortfolioContext:
        """
        Execute complete Portfolio Engine.
        """

        self.logger.log_start(context)

        if not self.validator.validate(context):

            self.logger.log_failure(context)

            return context

        context = self.processor.process(
            context,
        )

        self.logger.log_success(context)

        return context