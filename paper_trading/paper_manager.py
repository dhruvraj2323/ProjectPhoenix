"""
=================================================
Project Phoenix
Paper Trading Manager
M54
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
    High-level manager responsible for
    executing the complete Paper Trading
    workflow.
    """

    def __init__(
        self,
    ) -> None:

        self._engine = PaperTradingEngine()

    @property
    def engine(
        self,
    ) -> PaperTradingEngine:
        """
        Return engine instance.
        """

        return self._engine

    def execute(
        self,
        context: PaperContext,
    ) -> PaperContext:
        """
        Execute Paper Trading Engine.
        """

        return self._engine.run(
            context,
        )