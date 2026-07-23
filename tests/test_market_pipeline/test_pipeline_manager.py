"""
=================================================
Project Phoenix
Unit Test
Pipeline Manager
=================================================
"""

from market_pipeline.pipeline_context import PipelineContext
from market_pipeline.pipeline_manager import PipelineManager


def test_pipeline_manager():

    manager = PipelineManager()

    context = PipelineContext(
        pipeline_id="PIPELINE-001",
        symbol="XAUUSD",
        timeframe="M1",
    )

    result = manager.run(context)

    assert result.completed is True
    assert result.approved is True
    assert result.decision == "PIPELINE_COMPLETED"

    print("\n===== Pipeline Manager =====")
    print("Pipeline ID :", result.pipeline_id)
    print("Symbol      :", result.symbol)
    print("Timeframe   :", result.timeframe)
    print("Completed   :", result.completed)
    print("Approved    :", result.approved)
    print("Decision    :", result.decision)
    print("Reason      :", result.reason)
    print()

    print("Pipeline Manager Test Passed")


if __name__ == "__main__":
    test_pipeline_manager()