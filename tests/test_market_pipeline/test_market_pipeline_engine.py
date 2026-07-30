"""
=================================================
Project Phoenix
Unit Test
Pipeline Manager
M40.X.1
=================================================
"""

from market_pipeline.pipeline_context import PipelineContext
from market_pipeline.pipeline_manager import PipelineManager


TEST_DATA = "tests/test_data/sample_xauusd.zip"


def test_pipeline_manager():

    manager = PipelineManager()

    context = PipelineContext(
        pipeline_id="PIPELINE-001",
        symbol="XAUUSD",
        timeframe="M1",
        market_data_source=TEST_DATA,
    )

    result = manager.run(context)

    # -------------------------------------------------
    # Basic Validation
    # -------------------------------------------------

    assert result.completed is True
    assert result.approved is True
    assert result.failed is False

    # -------------------------------------------------
    # Decision
    # -------------------------------------------------

    assert result.decision == "PIPELINE_COMPLETED"

    # -------------------------------------------------
    # Market Data Validation
    # -------------------------------------------------

    market_data = result.get_metadata("market_data")

    assert market_data is not None
    assert market_data.success is True

    assert len(result.candles) > 0
    assert len(result.candles) == len(market_data.candles)

    # -------------------------------------------------
    # Indicators
    # -------------------------------------------------

    assert isinstance(result.indicators, dict)
    assert "ema" in result.indicators
    assert "rsi" in result.indicators
    assert "atr" in result.indicators

    # -------------------------------------------------
    # Patterns
    # -------------------------------------------------

    assert isinstance(result.patterns, list)

    print()
    print("===== Pipeline Manager =====")
    print("Pipeline ID     :", result.pipeline_id)
    print("Symbol          :", result.symbol)
    print("Timeframe       :", result.timeframe)
    print("Candles Loaded  :", len(result.candles))
    print("Completed       :", result.completed)
    print("Approved        :", result.approved)
    print("Decision        :", result.decision)
    print("Reason          :", result.reason)
    print()

    print("Pipeline Manager Test Passed")


if __name__ == "__main__":
    test_pipeline_manager()