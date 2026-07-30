"""
=================================================
Project Phoenix
Market Pipeline
Unit Test - Pipeline Engine
M40.X.1
=================================================
"""

from market_pipeline.pipeline_context import PipelineContext
from market_pipeline.pipeline_engine import PipelineEngine


TEST_DATA = "tests/test_data/sample_xauusd.zip"


def test_pipeline_engine():

    engine = PipelineEngine()

    context = PipelineContext(
        pipeline_id="PIPELINE-001",
        symbol="XAUUSD",
        timeframe="M1",
        market_data_source=TEST_DATA,
    )

    result = engine.run(context)

    # -------------------------------------------------
    # Basic Validation
    # -------------------------------------------------

    assert result.completed is True
    assert result.approved is True
    assert result.failed is False

    # -------------------------------------------------
    # Market Data Validation
    # -------------------------------------------------

    assert len(result.candles) > 0

    market_data = result.get_metadata("market_data")

    assert market_data is not None
    assert market_data.success is True
    assert len(market_data.candles) == len(result.candles)

    # -------------------------------------------------
    # Decision
    # -------------------------------------------------

    assert result.decision == "PIPELINE_COMPLETED"

    print()
    print("===== Pipeline Engine =====")
    print("Pipeline ID     :", result.pipeline_id)
    print("Symbol          :", result.symbol)
    print("Timeframe       :", result.timeframe)
    print("Candles Loaded  :", len(result.candles))
    print("Approved        :", result.approved)
    print("Completed       :", result.completed)
    print("Decision        :", result.decision)
    print("Reason          :", result.reason)
    print()

    print("Pipeline Engine Test Passed")


if __name__ == "__main__":
    test_pipeline_engine()