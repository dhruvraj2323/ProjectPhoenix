"""
=================================================
Project Phoenix
System Integration Engine
=================================================

Master controller for the complete
Project Phoenix integration pipeline.
"""

from integration.integration_logger import IntegrationLogger
from integration.integration_models import (
    ExecutionSummary,
    IntegrationResult,
    SystemHealth,
)
from integration.integration_pipeline import IntegrationPipeline
from integration.integration_validator import IntegrationValidator


class IntegrationEngine:
    """
    Executes the complete integration workflow.
    """

    def run(self) -> IntegrationResult:

        # -----------------------------------------
        # Build Pipeline
        # -----------------------------------------

        pipeline = IntegrationPipeline()

        pipeline.build_pipeline()

        # -----------------------------------------
        # Validate
        # -----------------------------------------

        validation = IntegrationValidator(
            pipeline
        ).validate()

        # -----------------------------------------
        # Health
        # -----------------------------------------

        health = SystemHealth(
            healthy=validation.valid,
            total_modules=len(
                pipeline.get_pipeline()
            ),
            completed_modules=pipeline.completed_stages(),
            failed_modules=pipeline.failed_stages(),
        )

        # -----------------------------------------
        # Summary
        # -----------------------------------------

        summary = ExecutionSummary(
            execution_time_ms=0.0,
            completed_stages=pipeline.completed_stages(),
            failed_stages=pipeline.failed_stages(),
        )

        # -----------------------------------------
        # Final Result
        # -----------------------------------------

        result = IntegrationResult(
            status=(
                "APPROVED"
                if validation.valid
                else "FAILED"
            ),
            approved=validation.valid,
            validation=validation,
            health=health,
            summary=summary,
            stages={
                stage.name: stage.completed
                for stage in pipeline.get_pipeline()
            },
        )

        # -----------------------------------------
        # Logging
        # -----------------------------------------

        IntegrationLogger.log(result)

        return result