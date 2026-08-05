"""
=================================================
Project Phoenix
Live Pipeline
M58.12.3
=================================================
"""

from __future__ import annotations

from deployment.live_market_data import (
    LiveMarketData,
)

from market_pipeline.market_pipeline_engine import (
    MarketPipelineEngine,
)


class LivePipeline:
    """
    Executes the real Market Pipeline
    using live MT5 connectivity.
    """

    def __init__(
        self,
    ) -> None:

        self.market = LiveMarketData()

        self.pipeline = MarketPipelineEngine()

    # --------------------------------------------------
    # Execute
    # --------------------------------------------------

    def execute(
        self,
        symbol: str,
        bars: int = 500,
    ) -> dict:

        if not self.market.connect():

            return {}

        try:

            market_data = self.market.get_multi_timeframe_data(

                symbol=symbol,

                bars=bars,

            )

            results = {}

            for timeframe in market_data:

                if len(market_data[timeframe]) == 0:

                    continue

                results[timeframe] = self.pipeline.run(

                    pipeline_id=f"LIVE-{timeframe}",

                    symbol=symbol,

                    timeframe=timeframe,

                )

            return results

        finally:

            self.market.disconnect()