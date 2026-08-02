"""
=================================================
Project Phoenix
Live Trading Manager
M55
=================================================
"""

from __future__ import annotations

from live_trading.live_context import LiveContext
from live_trading.live_engine import LiveTradingEngine


class LiveManager:
    """
    High-level manager for
    Live Trading Engine.
    """

    def __init__(self) -> None:

        self.engine = LiveTradingEngine()

    def run(
        self,
        context: LiveContext,
    ) -> LiveContext:
        """
        Execute Live Trading workflow.
        """

        return self.engine.run(context)