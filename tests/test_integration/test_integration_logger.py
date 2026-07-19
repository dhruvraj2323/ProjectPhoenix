"""
=================================================
Project Phoenix
Integration Logger Test
=================================================
"""

from integration.integration_logger import (
    IntegrationLogger,
)

from integration.integration_models import (
    ExecutionSummary,
    IntegrationResult,
    SystemHealth,
    ValidationResult,
)


def run_test():

    validation = ValidationResult(
        valid=True,
        reason="System integration validation passed.",
    )

    health = SystemHealth(
        healthy=True,
        total_modules=15,
        completed_modules=15,
        failed_modules=0,
    )

    summary = ExecutionSummary(
        execution_time_ms=12.350,
        completed_stages=15,
        failed_stages=0,
    )

    result = IntegrationResult(
        status="APPROVED",
        approved=True,
        validation=validation,
        health=health,
        summary=summary,
        stages={},
    )

    IntegrationLogger.log(result)

    assert result.approved

    print()
    print("Integration Logger Test Passed")


if __name__ == "__main__":

    run_test()