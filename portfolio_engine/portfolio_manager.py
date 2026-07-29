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
    High-level interface for Portfolio Engine.
    """

    def __init__(self) -> None:

        self.engine = PortfolioEngine()

    def update(
        self,
        context: PortfolioContext,
    ) -> PortfolioContext:
        """
        Execute complete portfolio workflow.
        """

        return self.engine.run(
            context,
        )