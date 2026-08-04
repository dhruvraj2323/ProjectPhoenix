"""
=================================================
Project Phoenix
Engine Router
M56.1
=================================================
"""

from __future__ import annotations

from live_trading.live_engine import LiveTradingEngine
from paper_trading.paper_engine import PaperTradingEngine


class EngineRouter:
    """
    Routes execution to the appropriate
    trading engine.
    """

    def __init__(self) -> None:

        self.paper_engine = PaperTradingEngine()

        self.live_engine = LiveTradingEngine()

    def route(
        self,
        context,
        live_mode: bool = False,
    ):
        """
        Route execution based on mode.
        """

        if live_mode:

            return self.live_engine.run(context)

        return self.paper_engine.run(context)