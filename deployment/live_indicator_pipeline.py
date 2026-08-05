"""
=================================================
Project Phoenix
Live Indicator Pipeline
M58.12.4
=================================================
"""

from __future__ import annotations

from deployment.live_market_data import (
    LiveMarketData,
)

from indicator_engine.indicator_context import (
    IndicatorContext,
)

from indicator_engine.indicator_engine import (
    IndicatorEngine,
)


class LiveIndicatorPipeline:
    """
    Executes the existing Indicator Engine
    using live MT5 candle data.
    """

    def __init__(
        self,
    ) -> None:

        self.market = LiveMarketData()

        self.engine = IndicatorEngine()

    # --------------------------------------------------

    def execute(
        self,
        symbol: str,
        timeframe: str = "M15",
        bars: int = 500,
    ) -> IndicatorContext | None:

        if not self.market.connect():

            return None

        try:

            candles = self.market.get_candles(

                symbol=symbol,

                timeframe=timeframe,

                bars=bars,

            )

            context = IndicatorContext(

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