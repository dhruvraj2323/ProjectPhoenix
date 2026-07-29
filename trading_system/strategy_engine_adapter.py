"""
=================================================
Project Phoenix
Strategy Engine Adapter
M40.2
=================================================
"""

from __future__ import annotations

from trading_system.trading_context import (
    TradingContext,
)


class StrategyEngineAdapter:
    """
    Adapter for Strategy Engine.
    """

    def __init__(
        self,
        strategy_engine,
    ) -> None:

        self.strategy_engine = strategy_engine

    def execute(
        self,
        context: TradingContext,
    ) -> TradingContext:
        """
        Execute Strategy Engine.
        """

        result = self.strategy_engine.execute(
            candles=context.candles,
            indicators=context.indicators,
            patterns=context.patterns,
        )

        context.strategy_name = result.get(
            "strategy_name",
            "",
        )

        context.signal = result.get(
            "signal",
            "",
        )

        context.signal_strength = result.get(
            "signal_strength",
            0.0,
        )

        return context