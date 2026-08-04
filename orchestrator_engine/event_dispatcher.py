"""
=================================================
Project Phoenix
Event Dispatcher
M56
=================================================
"""

from __future__ import annotations

from live_trading.live_context import LiveContext
from orchestrator_engine.engine_router import EngineRouter
from paper_trading.paper_context import PaperContext


class EventDispatcher:
    """
    Dispatches execution requests
    to the appropriate trading engine.
    """

    def __init__(
        self,
    ) -> None:

        self.router = EngineRouter()

    def dispatch(
        self,
        context: PaperContext | LiveContext,
        live_mode: bool = False,
    ):
        """
        Dispatch execution request.
        """

        return self.router.route(
            context=context,
            live_mode=live_mode,
        )