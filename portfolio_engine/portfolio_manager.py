"""
=================================================
Project Phoenix
Portfolio Manager
M35
=================================================
"""

from __future__ import annotations

from portfolio_engine.portfolio_context import (
    PortfolioContext,
)

from portfolio_engine.portfolio_engine import (
    PortfolioEngine,
)


class PortfolioManager:
    """
    Public entry point for Portfolio Engine.
    """

    def __init__(self) -> None:

        self.engine = PortfolioEngine()

    def execute(
        self,
        context: PortfolioContext,
    ) -> PortfolioContext:
        """
        Execute Portfolio Engine.
        """

        return self.engine.run(
            context,
        )