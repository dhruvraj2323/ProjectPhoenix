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
    High-level interface for Risk Engine.
    """

    def __init__(self) -> None:

        self.engine = RiskEngine()

    def evaluate(
        self,
        context: RiskContext,
    ) -> RiskContext:
        """
        Evaluate account risk.
        """

        return self.engine.run(
            context,
        )