"""
=================================================
Project Phoenix
Market Pipeline
Unit Test - Pipeline Context
=================================================
"""

from market_pipeline.pipeline_context import PipelineContext


def test_pipeline_context():

    context = PipelineContext(
        pipeline_id="PIPELINE-001",
        symbol="XAUUSD",
        timeframe="M1",
    )

    # ---------------------------------------
    # Metadata
    # ---------------------------------------

    context.set_metadata("broker", "MT5")
    context.set_metadata("mode", "PAPER")

    assert context.get_metadata("broker") == "MT5"
    assert context.get_metadata("mode") == "PAPER"
    assert context.get_metadata("unknown", "N/A") == "N/A"

    # ---------------------------------------
    # Approval
    # ---------------------------------------

    context.approve(
        decision="APPROVE",
        reason="Pipeline completed successfully."
    )

    assert context.approved is True
    assert context.completed is True
    assert context.failed is False

    # ---------------------------------------
    # Reset
    # ---------------------------------------

    context.reset()

    assert context.approved is False
    assert context.completed is False
    assert context.failed is False
    assert context.metadata == {}

    print("===== Pipeline Context =====")
    print("Pipeline ID :", context.pipeline_id)
    print("Symbol      :", context.symbol)
    print("Timeframe   :", context.timeframe)
    print("Approved    :", context.approved)
    print("Completed   :", context.completed)
    print("Failed      :", context.failed)
    print()

    print("Pipeline Context Test Passed")


if __name__ == "__main__":
    test_pipeline_context()