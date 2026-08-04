"""
=================================================
Project Phoenix
Session Controller
M56
=================================================
"""

from __future__ import annotations

from live_trading.live_context import LiveContext
from orchestrator_engine.event_dispatcher import (
    EventDispatcher,
)
from paper_trading.paper_context import (
    PaperContext,
)


class SessionController:
    """
    Controls a complete
    orchestration session.
    """

    def __init__(
        self,
    ) -> None:

        self.dispatcher = (
            EventDispatcher()
        )

    def execute(
        self,
        context: PaperContext | LiveContext,
        live_mode: bool = False,
    ):
        """
        Execute one complete
        orchestration session.
        """

        context.set_metadata(
            "session_started",
            True,
        )

        context = (
            self.dispatcher.dispatch(
                context=context,
                live_mode=live_mode,
            )
        )

        context.set_metadata(
            "session_completed",
            context.completed,
        )

        return context