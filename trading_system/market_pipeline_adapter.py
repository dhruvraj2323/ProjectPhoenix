"""
=================================================
Project Phoenix
Market Pipeline Adapter
M40.1
=================================================
"""

from __future__ import annotations

from typing import Any

from trading_system.trading_context import TradingContext


class MarketPipelineAdapter:
    """
    Adapter between Trading System and
    Market Pipeline Engine.
    """

    def __init__(
        self,
        pipeline: Any,
    ) -> None:
        self.pipeline = pipeline

    def execute(
        self,
        context: TradingContext,
    ) -> TradingContext:
        """
        Execute Market Pipeline.
        """

        result = self.pipeline.execute(
            symbol=context.symbol,
            timeframe=context.timeframe,
        )

        context.market_data = result

        context.metadata["market_pipeline"] = "SUCCESS"

        return context