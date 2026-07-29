"""
=================================================
Project Phoenix
AI Engine Adapter
M40.4
=================================================
"""

from __future__ import annotations

from trading_system.trading_context import TradingContext


class AIEngineAdapter:
    """
    Adapter for AI Engine.
    """

    def __init__(
        self,
        ai_engine,
    ) -> None:

        self.ai_engine = ai_engine

    def execute(
        self,
        context: TradingContext,
    ) -> TradingContext:
        """
        Execute AI Engine.
        """

        result = self.ai_engine.execute(
            signal=context.signal,
            signal_strength=context.signal_strength,
            risk_score=context.risk_score,
        )

        context.ai_score = result.get(
            "ai_score",
            0.0,
        )

        context.ai_confidence = result.get(
            "ai_confidence",
            0.0,
        )

        context.ai_decision = result.get(
            "ai_decision",
            "",
        )

        return context