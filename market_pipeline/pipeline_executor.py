"""
=================================================
Project Phoenix
Market Pipeline Executor
M40.X.4 - Signal Engine Integration
=================================================
"""

from __future__ import annotations

from indicator_engine.indicator_context import IndicatorContext
from indicator_engine.indicator_manager import IndicatorManager
from market_data.market_data_manager import MarketDataManager

from market_pipeline.pipeline_context import PipelineContext
from market_pipeline.pipeline_logger import PipelineLogger
from market_pipeline.pipeline_models import PipelineStage
from market_pipeline.pipeline_router import PipelineRouter

from pattern_engine.pattern_context import PatternContext
from pattern_engine.pattern_manager import PatternManager

from signal_engine.signal_context import SignalContext
from signal_engine.signal_manager import SignalManager


class PipelineExecutor:
    """
    Executes the complete Project Phoenix Market Pipeline.

    Stages

    - Market Data
    - Indicator Engine
    - Pattern Engine
    - Signal Engine
    - Risk Engine
    - Portfolio Engine
    - AI Engine
    - Execution Engine
    """

    def __init__(self) -> None:

        self.router = PipelineRouter()
        self.logger = PipelineLogger()

        # Integrated Managers
        self.market_data_manager = MarketDataManager()
        self.indicator_manager = IndicatorManager()
        self.pattern_manager = PatternManager()
        self.signal_manager = SignalManager()

    # ---------------------------------------------------------

    def execute(
        self,
        context: PipelineContext,
    ) -> PipelineContext:
        """
        Execute the complete market pipeline.
        """

        current_stage = PipelineStage.INITIALIZED

        while self.router.has_next_stage(current_stage):

            next_stage = self.router.get_next_stage(
                current_stage
            )

            if next_stage is None:
                break

            context.current_stage = next_stage

            self._execute_stage(
                next_stage,
                context,
            )

            if context.failed:
                break

            self.logger.log_stage(
                context
            )

            current_stage = next_stage

        if not context.failed:
            context.completed = True

        return context

    # ---------------------------------------------------------

    def _execute_stage(
        self,
        stage: PipelineStage,
        context: PipelineContext,
    ) -> None:

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
    # Market Data
    # =========================================================

    def _market_data(
        self,
        context: PipelineContext,
    ) -> None:

        market_data = self.market_data_manager.process(
            context.market_data_source,
            context.timeframe,
        )

        if not market_data.success:

            context.reject(
                decision="MARKET_DATA_FAILED",
                reason="; ".join(
                    market_data.errors
                ),
            )

            return

        context.candles = market_data.candles

        context.set_metadata(
            "market_data",
            market_data,
        )

    # =========================================================
    # Indicator Engine
    # =========================================================

    def _indicators(
        self,
        context: PipelineContext,
    ) -> None:

        indicator_context = IndicatorContext(
            engine_id=context.pipeline_id,
            symbol=context.symbol,
            timeframe=context.timeframe,
            candles=context.candles,
        )

        indicator_context = self.indicator_manager.run(
            indicator_context
        )

        if indicator_context.failed:

            context.reject(
                decision="INDICATOR_ENGINE_FAILED",
                reason=indicator_context.reason,
            )

            return

        context.indicators = (
            indicator_context.indicators
        )

        context.set_metadata(
            "indicator_context",
            indicator_context,
        )

    # =========================================================
    # Pattern Engine
    # =========================================================

    def _patterns(
        self,
        context: PipelineContext,
    ) -> None:

        pattern_context = PatternContext(
            engine_id=context.pipeline_id,
            symbol=context.symbol,
            timeframe=context.timeframe,
            candles=context.candles,
        )

        pattern_context = self.pattern_manager.run(
            pattern_context
        )

        if pattern_context.failed:

            context.reject(
                decision="PATTERN_ENGINE_FAILED",
                reason=pattern_context.reason,
            )

            return

        context.patterns = (
            pattern_context.patterns
        )

        context.set_metadata(
            "pattern_context",
            pattern_context,
        )

    # =========================================================
    # Signal Engine
    # =========================================================

    def _signal(
        self,
        context: PipelineContext,
    ) -> None:

        signal_context = SignalContext(
            engine_id=context.pipeline_id,
            symbol=context.symbol,
            timeframe=context.timeframe,
            indicators=context.indicators,
            patterns=context.patterns,
        )

        signal_context = self.signal_manager.run(
            signal_context
        )

        if signal_context.failed:

            context.reject(
                decision="SIGNAL_ENGINE_FAILED",
                reason=signal_context.reason,
            )

            return

        context.signals = (
            signal_context.signals
        )

        context.set_metadata(
            "signal_context",
            signal_context,
        )

    # =========================================================
    # Risk Engine
    # =========================================================

    def _risk(
        self,
        context: PipelineContext,
    ) -> None:

        context.risk_result = {
            "approved": True,
        }

    # =========================================================
    # Portfolio Engine
    # =========================================================

    def _portfolio(
        self,
        context: PipelineContext,
    ) -> None:

        context.portfolio_result = {
            "approved": True,
        }

    # =========================================================
    # AI Engine
    # =========================================================

    def _ai(
        self,
        context: PipelineContext,
    ) -> None:

        context.ai_result = {
            "approved": True,
        }

    # =========================================================
    # Execution Engine
    # =========================================================

    def _execution(
        self,
        context: PipelineContext,
    ) -> None:

        context.execution_result = {
            "executed": False,
        }

        context.approve(
            decision="PIPELINE_COMPLETED",
            reason="Pipeline executed successfully.",
        )