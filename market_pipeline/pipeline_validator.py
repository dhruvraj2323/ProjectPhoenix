"""
=================================================
Project Phoenix
Pipeline Validator
M31
=================================================
"""

from market_pipeline.pipeline_context import PipelineContext


class PipelineValidator:
    """
    Validates PipelineContext before execution.
    """

    def validate(
        self,
        context: PipelineContext,
    ) -> bool:
        """
        Validate pipeline context.
        """

        if not context.pipeline_id:
            context.reject(
                decision="INVALID_PIPELINE",
                reason="Pipeline ID missing.",
            )
            return False

        if not context.symbol:
            context.reject(
                decision="INVALID_SYMBOL",
                reason="Symbol missing.",
            )
            return False

        if not context.timeframe:
            context.reject(
                decision="INVALID_TIMEFRAME",
                reason="Timeframe missing.",
            )
            return False

        return True