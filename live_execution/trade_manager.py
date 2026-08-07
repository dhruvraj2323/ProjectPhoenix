"""
=================================================
Project Phoenix
Trade Manager
M59.1.9
=================================================
"""

from __future__ import annotations

from live_execution.trade_context import (
    TradeContext,
)

from live_execution.trade_engine import (
    TradeEngine,
)


class TradeManager:
    """
    High-level manager for the
    Live Trade Execution Engine.

    Acts as the public interface used by
    Project Phoenix Deployment.
    """

    def __init__(
        self,
    ) -> None:

        self.engine = TradeEngine()

    # --------------------------------------------------

    def execute(
        self,
        context: TradeContext,
    ) -> TradeContext:
        """
        Execute complete
        Live Trade Engine.
        """

        return self.engine.run(
            context,
        )