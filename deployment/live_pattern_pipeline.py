"""
=================================================
Project Phoenix
Live Pattern Pipeline
M58.12.5
=================================================
"""

from __future__ import annotations

from deployment.live_market_data import (
    LiveMarketData,
)

from deployment.market_data_adapter import (
    MarketDataAdapter,
)

from pattern_engine.pattern_context import (
    PatternContext,
)

from pattern_engine.pattern_engine import (
    PatternEngine,
)


class LivePatternPipeline:
    """
    Executes the existing Pattern Engine
    using normalized live MT5 candles.
    """

    def __init__(
        self,
    ) -> None:

        self.market = LiveMarketData()

        self.adapter = MarketDataAdapter()

        self.engine = PatternEngine()

    # --------------------------------------------------

    def execute(
        self,
        symbol: str,
        timeframe: str = "M15",
        bars: int = 500,
    ) -> PatternContext | None:

        if not self.market.connect():

            return None

        try:

            candles = self.market.get_candles(

                symbol=symbol,

                timeframe=timeframe,

                bars=bars,

            )

            candles = self.adapter.normalize(
                candles
            )

            context = PatternContext(

                engine_id=f"LIVE-{timeframe}",

                symbol=symbol,

                timeframe=timeframe,

            )

            context.candles = candles

            return self.engine.run(
                context
            )

        finally:

            self.market.disconnect()