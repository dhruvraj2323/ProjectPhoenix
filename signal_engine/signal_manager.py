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
    High-level manager for the Signal Engine.

    Acts as the public interface used by
    the Orchestrator Engine.
    """

    def __init__(self) -> None:

        self.engine = SignalEngine()

    # ---------------------------------------------------------

    def execute(
        self,
        context: SignalContext,
    ) -> SignalContext:
        """
        Execute the complete Signal Engine.
        """

        return self.engine.run(
            context,
        )

    # ---------------------------------------------------------

    def run(
        self,
        context: SignalContext,
    ) -> SignalContext:
        """
        Backward compatibility wrapper.
        """

        return self.execute(
            context,
        )