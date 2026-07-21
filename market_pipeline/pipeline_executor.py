"""
=================================================
Project Phoenix
Market Pipeline Executor
M31
=================================================
"""

from __future__ import annotations

from market_pipeline.pipeline_context import PipelineContext
from market_pipeline.pipeline_models import PipelineStage
from market_pipeline.pipeline_router import PipelineRouter
from market_pipeline.pipeline_logger import PipelineLogger


class PipelineExecutor:
    """
    Executes the Project Phoenix Market Pipeline.

    The executor walks through every pipeline stage
    sequentially using the PipelineRouter.

    Every stage updates the shared PipelineContext.
    """

    def __init__(self) -> None:

        self.router = PipelineRouter()

        # Added Logger
        self.logger = PipelineLogger()

    # ---------------------------------------------------------

    def execute(self, context: PipelineContext) -> PipelineContext:
        """
        Execute the complete pipeline.
        """

        current_stage = PipelineStage.INITIALIZED

        while self.router.has_next_stage(current_stage):

            next_stage = self.router.get_next_stage(current_stage)

            if next_stage is None:
                break

            context.current_stage = next_stage

            self._execute_stage(next_stage, context)

            # Log every completed stage
            self.logger.log_stage(context)

            current_stage = next_stage

        context.completed = True

        return context

    # ---------------------------------------------------------

    def _execute_stage(
        self,
        stage: PipelineStage,
        context: PipelineContext,
    ) -> None:
        """
        Execute one pipeline stage.
        """

        if stage == PipelineStage.MARKET_DATA:
            self._market_data(context)

        elif stage == PipelineStage.INDICATORS:
            self._indicators(context)

        elif stage == PipelineStage.PATTERNS:
            self._patterns(context)

        elif stage == PipelineStage.SIGNAL:
            self._signal(context)

        elif stage == PipelineStage.RISK:
            self._risk(context)

        elif stage == PipelineStage.PORTFOLIO:
            self._portfolio(context)

        elif stage == PipelineStage.AI:
            self._ai(context)

        elif stage == PipelineStage.EXECUTION:
            self._execution(context)

    # =========================================================
    # Individual Pipeline Stages
    # =========================================================

    def _market_data(
        self,
        context: PipelineContext,
    ) -> None:
        """
        Market Data Stage
        """

        context.set_metadata(
            "market_data",
            "Loaded"
        )

    # ---------------------------------------------------------

    def _indicators(
        self,
        context: PipelineContext,
    ) -> None:
        """
        Indicator Stage
        """

        context.indicators = {
            "ema": None,
            "rsi": None,
            "atr": None,
        }

    # ---------------------------------------------------------

    def _patterns(
        self,
        context: PipelineContext,
    ) -> None:
        """
        Pattern Recognition Stage
        """

        context.patterns = []

    # ---------------------------------------------------------

    def _signal(
        self,
        context: PipelineContext,
    ) -> None:
        """
        Signal Generation Stage
        """

        context.signal = None

    # ---------------------------------------------------------

    def _risk(
        self,
        context: PipelineContext,
    ) -> None:
        """
        Risk Engine Stage
        """

        context.risk_result = {
            "approved": True
        }

    # ---------------------------------------------------------

    def _portfolio(
        self,
        context: PipelineContext,
    ) -> None:
        """
        Portfolio Stage
        """

        context.portfolio_result = {
            "approved": True
        }

    # ---------------------------------------------------------

    def _ai(
        self,
        context: PipelineContext,
    ) -> None:
        """
        AI Validation Stage
        """

        context.ai_result = {
            "approved": True
        }

    # ---------------------------------------------------------

    def _execution(
        self,
        context: PipelineContext,
    ) -> None:
        """
        Execution Stage
        """

        context.execution_result = {
            "executed": False
        }

        context.approve(
            decision="PIPELINE_COMPLETED",
            reason="Pipeline executed successfully."
        )