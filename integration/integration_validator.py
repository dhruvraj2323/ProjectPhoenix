"""
=================================================
Project Phoenix
System Integration Validator
=================================================

Validates the complete integration pipeline.
"""

from integration.integration_models import (
    ValidationResult,
)
from integration.integration_pipeline import (
    IntegrationPipeline,
)


class IntegrationValidator:
    """
    Validates the complete Project Phoenix
    integration pipeline.
    """

    def __init__(self, pipeline: IntegrationPipeline):

        self.pipeline = pipeline

    # -------------------------------------------------

    def validate(self) -> ValidationResult:
        """
        Validate pipeline execution.
        """

        if self.pipeline.completed_stages() == 0:

            return ValidationResult(
                valid=False,
                reason="Pipeline contains no completed stages.",
            )

        if self.pipeline.failed_stages() > 0:

            return ValidationResult(
                valid=False,
                reason="One or more pipeline stages failed.",
            )

        return ValidationResult(
            valid=True,
            reason="System integration validation passed.",
        )