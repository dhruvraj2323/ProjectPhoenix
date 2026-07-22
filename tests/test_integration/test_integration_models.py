"""
=================================================
Project Phoenix
System Integration Models Test
=================================================
"""

from integration.integration_models import (
    ExecutionSummary,
    IntegrationResult,
    IntegrationStatus,
    PipelineStage,
    SystemHealth,
    ValidationResult,
)


# -------------------------------------------------
# Test
# -------------------------------------------------


def run_test():

    stage = PipelineStage(
        name="Configuration",
        completed=True,
        execution_time_ms=2.45,
        message="Loaded successfully.",
    )

    validation = ValidationResult(
        valid=True,
        reason="Pipeline validation passed.",
    )

    health = SystemHealth(
        healthy=True,
        total_modules=16,
        completed_modules=16,
        failed_modules=0,
    )

    summary = ExecutionSummary(
        execution_time_ms=15.75,
        completed_stages=16,
        failed_stages=0,
    )

    status = IntegrationStatus(
        approved=True,
        pipeline_completed=True,
        stages=[stage],
        validation=validation,
        health=health,
        summary=summary,
    )

    result = IntegrationResult(
        status="APPROVED",
        approved=True,
        validation=validation,
        health=health,
        summary=summary,
        stages={
            "Configuration": True,
        },
    )

    # ---------------------------------------------

    assert stage.completed
    assert validation.valid
    assert health.healthy
    assert summary.completed_stages == 16
    assert status.approved
    assert result.approved

    # ---------------------------------------------

    print("===== Integration Models =====")

    print(f"Stage            : {stage.name}")
    print(f"Completed        : {stage.completed}")
    print(f"Execution Time   : {stage.execution_time_ms:.2f} ms")

    print()

    print(f"Validation       : {validation.valid}")
    print(f"Health           : {health.healthy}")
    print(f"Modules          : {health.completed_modules}/{health.total_modules}")

    print()

    print(f"Pipeline         : {status.pipeline_completed}")
    print(f"Approved         : {status.approved}")

    print()

    print(f"Result           : {result.status}")

    print()
    print("Integration Models Test Passed")


# -------------------------------------------------
# Main
# -------------------------------------------------

if __name__ == "__main__":
    run_test()