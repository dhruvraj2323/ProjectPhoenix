"""
=================================================
Project Phoenix
Market Pipeline
Unit Test - Pipeline Executor
=================================================
"""

from market_pipeline.pipeline_context import PipelineContext
from market_pipeline.pipeline_executor import PipelineExecutor
from market_pipeline.pipeline_models import PipelineStage


def test_pipeline_executor():

    context = PipelineContext(
        pipeline_id="PIPELINE-001",
        symbol="XAUUSD",
        timeframe="M1",
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
    # Metadata
    # -------------------------------------------------

    assert result.get_metadata("market_data") == "Loaded"

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

    print("===== Pipeline Executor =====")
    print("Pipeline ID   :", result.pipeline_id)
    print("Symbol        :", result.symbol)
    print("Timeframe     :", result.timeframe)
    print("Current Stage :", result.current_stage.value)
    print("Approved      :", result.approved)
    print("Completed     :", result.completed)
    print("Decision      :", result.decision)
    print("Reason        :", result.reason)
    print()

    print("Pipeline Executor Test Passed")


if __name__ == "__main__":
    test_pipeline_executor()