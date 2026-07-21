"""
=================================================
Project Phoenix
Market Pipeline
Unit Test - Pipeline Models
=================================================
"""

from market_pipeline.pipeline_models import (
    PipelineStage,
    PipelineStatus,
    PipelineResult,
    PipelineState,
)


def test_pipeline_models():

    state = PipelineState(
        symbol="XAUUSD",
        timeframe="M1",
        mode="PAPER"
    )

    result = PipelineResult(
        stage=PipelineStage.MARKET_DATA,
        status=PipelineStatus.SUCCESS,
        approved=True,
        reason="Market data loaded successfully."
    )

    state.results.append(result)
    state.current_stage = PipelineStage.MARKET_DATA

    assert state.symbol == "XAUUSD"
    assert state.timeframe == "M1"
    assert state.mode == "PAPER"

    assert state.current_stage == PipelineStage.MARKET_DATA

    assert result.approved is True
    assert result.status == PipelineStatus.SUCCESS
    assert result.stage == PipelineStage.MARKET_DATA

    print("===== Pipeline Models =====")
    print("Symbol        :", state.symbol)
    print("Timeframe     :", state.timeframe)
    print("Mode          :", state.mode)
    print("Current Stage :", state.current_stage.value)
    print("Approved      :", result.approved)
    print("Status        :", result.status.value)
    print("Reason        :", result.reason)
    print()

    print("Pipeline Models Test Passed")


if __name__ == "__main__":
    test_pipeline_models()