"""
=================================================
Project Phoenix
Market Pipeline Engine
M31
=================================================
"""

from __future__ import annotations

from market_pipeline.pipeline_context import PipelineContext
from market_pipeline.pipeline_engine import PipelineEngine
from market_pipeline.integration_models import (
    IntegrationModels,
    PipelineStatus,
    ProcessingStatistics,
    ValidationSummary,
)


class MarketPipelineEngine:
    """
    Top-level Market Pipeline Engine.

    This class bridges M30 and M31.
    """

    def __init__(self) -> None:

        self.engine = PipelineEngine()

        self.models = IntegrationModels()

    # ---------------------------------------------------------

    def run(
        self,
        pipeline_id: str,
        symbol: str,
        timeframe: str,
    ):

        context = PipelineContext(
            pipeline_id=pipeline_id,
            symbol=symbol,
            timeframe=timeframe,
        )

        context = self.engine.run(context)

        status = PipelineStatus(
            completed=context.completed,
            validation_passed=context.approved,
            stage=str(context.current_stage),
        )

        statistics = ProcessingStatistics(
            total_candles=len(context.candles),
            indicators_calculated=len(
                context.indicators
            ),
            patterns_detected=len(
                context.patterns
            ),
            processing_time=0.0,
        )

        validation = ValidationSummary(
            passed=context.approved,
            errors=0,
            warnings=0,
        )

        return self.models.create_pipeline_result(
            approved=context.approved,
            reason=context.reason,
            payload=context,
            status=status,
            statistics=statistics,
            validation=validation,
        )