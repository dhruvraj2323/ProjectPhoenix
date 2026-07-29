"""
=================================================
Project Phoenix
Unit Test
Market Pipeline Adapter
=================================================
"""

from trading_system.market_pipeline_adapter import (
    MarketPipelineAdapter,
)

from trading_system.trading_context import (
    TradingContext,
)


class DummyPipeline:
    """
    Dummy Market Pipeline.
    """

    def execute(
        self,
        symbol,
        timeframe,
    ):
        return {
            "symbol": symbol,
            "timeframe": timeframe,
            "status": "SUCCESS",
        }


def test_market_pipeline_adapter():

    context = TradingContext(
        trading_id="TRD-001",
        symbol="XAUUSD",
        timeframe="M1",
    )

    adapter = MarketPipelineAdapter(
        DummyPipeline(),
    )

    context = adapter.execute(
        context,
    )

    assert context.market_data["status"] == "SUCCESS"

    assert (
        context.metadata["market_pipeline"]
        == "SUCCESS"
    )

    print("\nMarket Pipeline Adapter Test Passed")


if __name__ == "__main__":

    test_market_pipeline_adapter()