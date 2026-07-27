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
    Pattern Engine and future Trading Engine.
    """

    def __init__(self) -> None:

        self.engine = SignalEngine()

    # ---------------------------------------------------------

    def run(
        self,
        context: SignalContext,
    ) -> SignalContext:
        """
        Execute the complete Signal Engine.
        """

        return self.engine.run(context)