"""
=================================================
Project Phoenix
Market Pipeline Validator
M31
=================================================
"""

from __future__ import annotations

from market_pipeline.pipeline_context import PipelineContext


class PipelineValidator:
    """
    Validates the pipeline context before and after
    execution.

    This validator ensures the pipeline has the
    minimum required information to continue safely.
    """

    # ---------------------------------------------------------

    def validate(self, context: PipelineContext) -> bool:
        """
        Run complete validation.
        """

        return (
            self._validate_symbol(context)
            and self._validate_timeframe(context)
            and self._validate_pipeline_id(context)
        )

    # ---------------------------------------------------------

    def _validate_pipeline_id(
        self,
        context: PipelineContext,
    ) -> bool:

        return bool(context.pipeline_id)

    # ---------------------------------------------------------

    def _validate_symbol(
        self,
        context: PipelineContext,
    ) -> bool:

        return bool(context.symbol)

    # ---------------------------------------------------------

    def _validate_timeframe(
        self,
        context: PipelineContext,
    ) -> bool:

        return bool(context.timeframe)

    # ---------------------------------------------------------

    def validation_report(
        self,
        context: PipelineContext,
    ) -> dict:
        """
        Return validation summary.
        """

        return {
            "pipeline_id": self._validate_pipeline_id(context),
            "symbol": self._validate_symbol(context),
            "timeframe": self._validate_timeframe(context),
            "overall": self.validate(context),
        }