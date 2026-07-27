"""
=================================================
Project Phoenix
Risk Manager
M36
=================================================
"""

from __future__ import annotations

from risk_engine.risk_context import RiskContext
from risk_engine.risk_engine import RiskEngine


class RiskManager:
    """
    High-level manager for the Risk Engine.

    Acts as the public interface used by
    Signal Engine and future Trading Engine.
    """

    def __init__(self) -> None:

        self.engine = RiskEngine()

    # ---------------------------------------------------------

    def run(
        self,
        context: RiskContext,
    ) -> RiskContext:
        """
        Execute the complete Risk Engine.
        """

        return self.engine.run(
            context,
        )