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
    High-level interface for the
    Paper Trading Engine.
    """

    def __init__(
        self,
    ) -> None:

        self.engine = (
            PaperTradingEngine()
        )

    # --------------------------------------------------
    # Execute
    # --------------------------------------------------

    def execute(
        self,
        context: PaperContext,
    ) -> PaperContext:
        """
        Execute complete
        Paper Trading workflow.
        """

        return self.engine.run(
            context,
        )

    # --------------------------------------------------
    # Reset
    # --------------------------------------------------

    def reset(
        self,
        context: PaperContext,
    ) -> PaperContext:
        """
        Reset Paper Trading context.
        """

        context.reset()

        return context

    # --------------------------------------------------
    # Validate
    # --------------------------------------------------

    def validate(
        self,
        context: PaperContext,
    ) -> bool:
        """
        Validate PaperContext using
        the underlying engine validator.
        """

        return self.engine.validator.validate(
            context,
        )        