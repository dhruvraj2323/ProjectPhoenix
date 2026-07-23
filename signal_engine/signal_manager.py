"""
=================================================
Project Phoenix
Signal Manager
M34
=================================================
"""

from __future__ import annotations

from signal_engine.signal_context import SignalContext
from signal_engine.signal_engine import SignalEngine


class SignalManager:
    """
    High-level interface for the Signal Engine.
    """

    def __init__(self) -> None:

        self.engine = SignalEngine()

    def execute(
        self,
        context: SignalContext,
    ) -> SignalContext:
        """
        Execute complete signal generation workflow.
        """

        return self.engine.run(context)