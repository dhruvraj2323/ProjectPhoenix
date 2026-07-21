"""
=================================================
Project Phoenix
Market Pipeline
Unit Test - Pipeline Logger
=================================================
"""

from market_pipeline.pipeline_context import PipelineContext
from market_pipeline.pipeline_logger import PipelineLogger
from market_pipeline.pipeline_models import PipelineStage


def test_pipeline_logger():

    logger = PipelineLogger()

    context = PipelineContext(
        pipeline_id="PIPELINE-001",
        symbol="XAUUSD",
        timeframe="M1",
    )

    logger.log_start(context)

    context.current_stage = PipelineStage.MARKET_DATA

    logger.log_stage(context)

    context.approve(
        decision="PIPELINE_COMPLETED",
        reason="Execution completed successfully."
    )

    logger.log_complete(context)

    assert context.approved is True
    assert context.completed is True

    print("===== Pipeline Logger =====")
    print("Pipeline ID :", context.pipeline_id)
    print("Stage       :", context.current_stage.value)
    print("Approved    :", context.approved)
    print()

    print("Pipeline Logger Test Passed")


if __name__ == "__main__":
    test_pipeline_logger()