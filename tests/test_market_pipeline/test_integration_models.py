"""
=================================================
Project Phoenix
Integration Models Test
=================================================
"""

from market_pipeline.integration_models import (
    PipelineStatus,
    ProcessingStatistics,
    ValidationSummary,
    PipelineResult,
)


def test_integration_models():

    status = PipelineStatus(
        completed=True,
        validation_passed=True,
        stage="Candlestick Engine",
    )

    statistics = ProcessingStatistics(
        total_candles=6052588,
        indicators_calculated=6,
        patterns_detected=35,
        processing_time=12.84,
    )

    validation = ValidationSummary(
        passed=True,
        errors=0,
        warnings=0,
    )

    result = PipelineResult(
        approved=True,
        reason="Market pipeline completed successfully.",
        status=status,
        statistics=statistics,
        validation=validation,
    )

    assert result.approved
    assert result.status.completed is True
    assert result.validation.passed is True
    assert result.statistics.total_candles == 6052588