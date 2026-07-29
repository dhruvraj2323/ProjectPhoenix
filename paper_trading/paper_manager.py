"""
=================================================
Project Phoenix
Paper Trading Manager
M24
=================================================
"""

from __future__ import annotations

from paper_trading.paper_context import (
    PaperContext,
)

from paper_trading.paper_engine import (
    PaperTradingEngine,
)


class PaperTradingManager:
    """
    High-level interface for
    Paper Trading Engine.
    """

    def __init__(self) -> None:

        self.engine = PaperTradingEngine()

    def execute(
        self,
        context: PaperContext,
    ) -> PaperContext:
        """
        Execute complete paper trading workflow.
        """

        return self.engine.run(
            context,
        )