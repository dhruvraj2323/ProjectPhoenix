"""
=================================================
Project Phoenix
Unit Test
Processing Report
=================================================
"""

from market_pipeline.pipeline_context import PipelineContext
from market_pipeline.processing_report import ProcessingReport


def test_processing_report():

    context = PipelineContext(
        pipeline_id="PIPELINE-001",
        symbol="XAUUSD",
        timeframe="M1",
    )

    context.indicators = {
        "EMA": 1,
        "RSI": 2,
        "ATR": 3,
    }

    context.patterns = [
        "DOJI",
        "HAMMER",
    ]

    context.set_metadata(
        "Broker",
        "MT5"
    )

    context.approve(
        decision="PIPELINE_COMPLETED",
        reason="Pipeline executed successfully."
    )

    report = ProcessingReport()

    report.print_report(context)

    print()
    print("Processing Report Test Passed")


if __name__ == "__main__":
    test_processing_report()