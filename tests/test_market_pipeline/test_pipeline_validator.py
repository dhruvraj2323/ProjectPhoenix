"""
=================================================
Project Phoenix
Market Pipeline
Unit Test - Pipeline Validator
=================================================
"""

from market_pipeline.pipeline_context import PipelineContext
from market_pipeline.pipeline_validator import PipelineValidator


def test_pipeline_validator():

    validator = PipelineValidator()

    context = PipelineContext(
        pipeline_id="PIPELINE-001",
        symbol="XAUUSD",
        timeframe="M1",
    )

    assert validator.validate(context) is True

    report = validator.validation_report(context)

    assert report["pipeline_id"] is True
    assert report["symbol"] is True
    assert report["timeframe"] is True
    assert report["overall"] is True

    print("===== Pipeline Validator =====")
    print("Pipeline ID :", report["pipeline_id"])
    print("Symbol      :", report["symbol"])
    print("Timeframe   :", report["timeframe"])
    print("Overall     :", report["overall"])
    print()

    print("Pipeline Validator Test Passed")


if __name__ == "__main__":
    test_pipeline_validator()