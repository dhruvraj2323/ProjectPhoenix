"""
=================================================
Project Phoenix
Pipeline Validator Test
=================================================
"""

from market_pipeline.pipeline_context import PipelineContext
from market_pipeline.pipeline_validator import PipelineValidator


def test_pipeline_validator():

    context = PipelineContext(
        pipeline_id="PIPE-001",
        symbol="EURUSD",
        timeframe="M5",
    )

    validator = PipelineValidator()

    result = validator.validate(context)

    print()
    print("Pipeline Validator Result")
    print("=========================")
    print(f"Validation Passed : {result}")

    assert result is True

    print()
    print("Pipeline Validator Test Passed")