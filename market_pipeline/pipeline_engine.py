"""
=================================================
Project Phoenix
Market Pipeline Engine
M31
=================================================
"""

from __future__ import annotations

from market_pipeline.pipeline_context import PipelineContext
from market_pipeline.pipeline_executor import PipelineExecutor
from market_pipeline.pipeline_logger import PipelineLogger
from market_pipeline.pipeline_validator import PipelineValidator


class PipelineEngine:
    """
    Main Market Pipeline Engine.

    Coordinates:

    - Validation
    - Logging
    - Execution

    into one unified pipeline.
    """

    def __init__(self) -> None:

        self.validator = PipelineValidator()

        self.executor = PipelineExecutor()

        self.logger = PipelineLogger()

    # ---------------------------------------------------------

    def run(
        self,
        context: PipelineContext,
    ) -> PipelineContext:
        """
        Execute the complete market pipeline.
        """

        self.logger.log_start(context)

        if not self.validator.validate(context):

            context.reject(
                decision="VALIDATION_FAILED",
                reason="Pipeline validation failed."
            )

            self.logger.log_failure(context)

            return context

        context = self.executor.execute(context)

        if context.approved:

            self.logger.log_complete(context)

        else:

            self.logger.log_failure(context)

        return context