"""
=================================================
Project Phoenix
Market Pipeline
Unit Test - Pipeline Engine
=================================================
"""

from market_pipeline.pipeline_context import PipelineContext
from market_pipeline.pipeline_engine import PipelineEngine


def test_pipeline_engine():

    engine = PipelineEngine()

    context = PipelineContext(
        pipeline_id="PIPELINE-001",
        symbol="XAUUSD",
        timeframe="M1",
    )

    result = engine.run(context)

    assert result.completed is True
    assert result.approved is True
    assert result.failed is False

    print("===== Pipeline Engine =====")
    print("Pipeline ID :", result.pipeline_id)
    print("Symbol      :", result.symbol)
    print("Timeframe   :", result.timeframe)
    print("Approved    :", result.approved)
    print("Completed   :", result.completed)
    print()

    print("Pipeline Engine Test Passed")


if __name__ == "__main__":
    test_pipeline_engine()