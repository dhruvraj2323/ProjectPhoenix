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


def run_test():

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

    print("===== Integration Models =====")
    print()

    print(f"Completed            : {status.completed}")
    print(f"Validation Passed    : {status.validation_passed}")
    print(f"Current Stage        : {status.stage}")

    print()

    print(f"Total Candles        : {statistics.total_candles}")
    print(f"Indicators           : {statistics.indicators_calculated}")
    print(f"Patterns             : {statistics.patterns_detected}")
    print(f"Processing Time      : {statistics.processing_time} sec")

    print()

    print(f"Validation Passed    : {validation.passed}")
    print(f"Errors               : {validation.errors}")
    print(f"Warnings             : {validation.warnings}")

    assert result.approved

    print()
    print("Integration Models Test Passed")


if __name__ == "__main__":
    run_test()