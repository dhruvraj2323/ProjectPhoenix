"""
=================================================
Project Phoenix
Market Pipeline
Unit Test - Pipeline Executor
M40.X.3 - Pattern Engine Integration
=================================================
"""

from market_data.market_data_models import MarketDataResult

from market_pipeline.pipeline_context import PipelineContext
from market_pipeline.pipeline_executor import PipelineExecutor
from market_pipeline.pipeline_models import PipelineStage


TEST_DATA = "tests/test_data/sample_xauusd.zip"


def test_pipeline_executor():

    context = PipelineContext(
        pipeline_id="PIPELINE-001",
        symbol="XAUUSD",
        timeframe="M1",
        market_data_source=TEST_DATA,
    )

    executor = PipelineExecutor()

    result = executor.execute(context)

    # -------------------------------------------------
    # Basic Validation
    # -------------------------------------------------

    assert result.completed is True
    assert result.approved is True
    assert result.failed is False

    # -------------------------------------------------
    # Final Stage
    # -------------------------------------------------

    assert result.current_stage == PipelineStage.COMPLETED

    # -------------------------------------------------
    # Market Data
    # -------------------------------------------------

    market_data = result.get_metadata("market_data")

    assert isinstance(
        market_data,
        MarketDataResult,
    )

    assert market_data.success is True
    assert len(market_data.candles) > 0

    assert result.candles == market_data.candles

    # -------------------------------------------------
    # Indicator Engine
    # -------------------------------------------------

    indicator_context = result.get_metadata(
        "indicator_context"
    )

    assert indicator_context is not None
    assert indicator_context.completed is True
    assert indicator_context.approved is True

    assert isinstance(result.indicators, dict)

    assert "EMA_20" in result.indicators
    assert "SMA_20" in result.indicators
    assert "RSI_14" in result.indicators
    assert "ATR_14" in result.indicators
    assert "MACD" in result.indicators
    assert "BOLLINGER_BANDS" in result.indicators
    assert "VWAP" in result.indicators
    assert "SUPERTREND" in result.indicators

    # -------------------------------------------------
    # Pattern Engine
    # -------------------------------------------------

    pattern_context = result.get_metadata(
        "pattern_context"
    )

    assert pattern_context is not None
    assert pattern_context.completed is True
    assert pattern_context.approved is True

    assert isinstance(result.patterns, list)

    assert result.patterns == pattern_context.patterns

    # -------------------------------------------------
    # Risk
    # -------------------------------------------------

    assert result.risk_result["approved"] is True

    # -------------------------------------------------
    # Portfolio
    # -------------------------------------------------

    assert result.portfolio_result["approved"] is True

    # -------------------------------------------------
    # AI
    # -------------------------------------------------

    assert result.ai_result["approved"] is True

    # -------------------------------------------------
    # Execution
    # -------------------------------------------------

    assert result.execution_result["executed"] is False

    print()
    print("===== Pipeline Executor =====")
    print("Pipeline ID      :", result.pipeline_id)
    print("Symbol           :", result.symbol)
    print("Timeframe        :", result.timeframe)
    print("Candles Loaded   :", len(result.candles))
    print("Indicators       :", len(result.indicators))
    print("Patterns         :", len(result.patterns))
    print("Current Stage    :", result.current_stage.value)
    print("Approved         :", result.approved)
    print("Completed        :", result.completed)
    print("Decision         :", result.decision)
    print("Reason           :", result.reason)
    print()

    print("Pipeline Executor Test Passed")


if __name__ == "__main__":
    test_pipeline_executor()