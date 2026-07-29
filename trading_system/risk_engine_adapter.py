"""
=================================================
Project Phoenix
Risk Engine Adapter
M40.3
=================================================
"""

from __future__ import annotations

from trading_system.trading_context import (
    TradingContext,
)


class RiskEngineAdapter:
    """
    Adapter for Risk Engine.
    """

    def __init__(
        self,
        risk_engine,
    ) -> None:

        self.risk_engine = risk_engine

    def execute(
        self,
        context: TradingContext,
    ) -> TradingContext:
        """
        Execute Risk Engine.
        """

        result = self.risk_engine.execute(

            signal=context.signal,

            signal_strength=context.signal_strength,

            symbol=context.symbol,

            timeframe=context.timeframe,

        )

        context.risk_score = result.get(

            "risk_score",

            0.0,

        )

        context.risk_passed = result.get(

            "risk_passed",

            False,

        )

        return context