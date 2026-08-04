"""
=================================================
Project Phoenix
Pipeline Runner
M58
=================================================
"""

from __future__ import annotations

from deployment.market_data_feed import (
    MarketDataFeed,
)

from market_pipeline.market_pipeline_engine import (
    MarketPipelineEngine,
)


class PipelineRunner:
    """
    Connects deployment with the
    Market Pipeline.
    """

    def __init__(
        self,
    ) -> None:

        self.feed = (
            MarketDataFeed()
        )

        self.pipeline = (
            MarketPipelineEngine()
        )

    # --------------------------------------------------
    # Execute
    # --------------------------------------------------

    def execute(
        self,
    ) -> bool:
        """
        Execute one market
        processing cycle.
        """

        market_data = (
            self.feed.fetch()
        )

        # --------------------------------------------------
        # Real MT5 candle processing
        # will replace this placeholder.
        # --------------------------------------------------

        if market_data is None:

            return False

        return True