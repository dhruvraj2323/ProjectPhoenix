"""
=================================================
Project Phoenix
Market Pipeline Executor
M40.X.8 - Execution Engine Integration
=================================================
"""

from __future__ import annotations

from ai_decision.ai_engine import AIEngine
from ai_decision.ai_models import (
    AIContext,
)

from execution_engine.execution_context import (
    ExecutionContext,
)
from execution_engine.execution_manager import (
    ExecutionManager,
)

from paper_trading.paper_context import (
    PaperContext,
)

from paper_trading.paper_manager import (
    PaperTradingManager,
)

from indicator_engine.indicator_context import IndicatorContext
from indicator_engine.indicator_manager import IndicatorManager

from market_data.market_data_manager import MarketDataManager

from market_pipeline.pipeline_context import PipelineContext
from market_pipeline.pipeline_logger import PipelineLogger
from market_pipeline.pipeline_models import PipelineStage
from market_pipeline.pipeline_router import PipelineRouter

from pattern_engine.pattern_context import PatternContext
from pattern_engine.pattern_manager import PatternManager

from portfolio_engine.portfolio_context import PortfolioContext
from portfolio_engine.portfolio_manager import PortfolioManager

from risk_engine.risk_context import RiskContext
from risk_engine.risk_manager import RiskManager

from signal_engine.signal_context import SignalContext
from signal_engine.signal_manager import SignalManager

from strategy.strategy_context import StrategyContext
from strategy.strategy_manager import StrategyManager


class PipelineExecutor:
    """
    Executes the complete Project Phoenix Market Pipeline.

    Stages

    - Market Data
    - Indicator Engine
    - Pattern Engine
    - Strategy Engine
    - Signal Engine
    - Risk Engine
    - Portfolio Engine
    - AI Engine
    - Execution Engine
    """

    def __init__(self) -> None:

        self.router = PipelineRouter()

        self.logger = PipelineLogger()

        self.market_data_manager = MarketDataManager()

        self.indicator_manager = IndicatorManager()

        self.pattern_manager = PatternManager()

        self.strategy_manager = StrategyManager()

        self.signal_manager = SignalManager()

        self.risk_manager = RiskManager()

        self.portfolio_manager = PortfolioManager()

        self.ai_engine = AIEngine()

        self.execution_manager = ExecutionManager()

        self.paper_manager = (
            PaperTradingManager()
        )

    # ---------------------------------------------------------

    def execute(
        self,
        context: PipelineContext,
    ) -> PipelineContext:

        current_stage = PipelineStage.INITIALIZED

        while self.router.has_next_stage(
            current_stage,
        ):

            next_stage = self.router.get_next_stage(
                current_stage,
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
                context,
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

        elif stage == PipelineStage.STRATEGY:

            self._strategy(context)        

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

        elif stage == PipelineStage.PAPER_TRADING:

            self._paper_trading(
                context,
            )

    # =========================================================
    # Market Data
    # =========================================================

    def _market_data(
        self,
        context: PipelineContext,
    ) -> None:
        """
        Load market data.

        Historical Mode:
            Load candles from MarketDataManager.

        Live Mode:
            Use candles already supplied by MT5.
        """

        # --------------------------------------------------
        # Live Trading Mode
        # --------------------------------------------------

        if context.candles:

            context.set_metadata(
                "market_data",
                "LIVE_MT5",
            )

            return

        # --------------------------------------------------
        # Historical Mode
        # --------------------------------------------------

        market_data = self.market_data_manager.process(

            context.market_data_source,

            context.timeframe,

        )

        if not market_data.success:

            context.reject(

                decision="MARKET_DATA_FAILED",

                reason="; ".join(
                    market_data.errors,
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
            indicator_context,
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
            pattern_context,
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
    # Strategy Engine
    # =========================================================

    def _strategy(
        self,
        context: PipelineContext,
    ) -> None:

        market_data = {}

        if context.candles:

            last_candle = context.candles[-1]

            if isinstance(last_candle, dict):

                market_data["price"] = (
                    last_candle.get(
                        "close",
                        0.0,
                    )
                )

        strategy_context = StrategyContext(

            engine_id=context.pipeline_id,

            symbol=context.symbol,

            timeframe=context.timeframe,

            indicators=context.indicators,

            patterns=context.patterns,

            market_data=market_data,

        )

        strategy_context = (
            self.strategy_manager.execute(
                strategy_context,
            )
        )     

        if not strategy_context.completed:

            context.reject(

                decision="STRATEGY_ENGINE_FAILED",

                reason=(
                    strategy_context.reason
                    or
                    "Strategy evaluation failed."
                ),

            )

            return

        context.strategy_result = (
            strategy_context.strategy_result
        )

        context.set_metadata(

            "strategy_context",

            strategy_context,

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
            signal_context,
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

        risk_context = RiskContext(

            engine_id=context.pipeline_id,

            account_id="SIM-001",

            balance=10000.0,

            equity=10000.0,

            free_margin=9800.0,

            # -----------------------------------------
            # M59.7
            # Market Intelligence
            # -----------------------------------------

            candles=context.candles,

            indicators=context.indicators,

            patterns=context.patterns,

            strategy_result=context.strategy_result,

        )

        risk_context = self.risk_manager.execute(
            risk_context,
        )

        if risk_context.failed:

            context.reject(

                decision="RISK_ENGINE_FAILED",

                reason=risk_context.reason,

            )

            return

        context.risk_result = (
            risk_context.risk_result
        )

        context.set_metadata(

            "risk_context",

            risk_context,

        )

    # =========================================================
    # Portfolio Engine
    # =========================================================

    def _portfolio(
        self,
        context: PipelineContext,
    ) -> None:

        portfolio_context = PortfolioContext(
            portfolio_id=context.pipeline_id,
            account_id="SIM-001",
        )

        portfolio_context = self.portfolio_manager.update(
            portfolio_context,
        )

        if portfolio_context.failed:

            context.reject(
                decision="PORTFOLIO_ENGINE_FAILED",
                reason=portfolio_context.reason,
            )

            return

        context.portfolio_result = (
            portfolio_context.summary
        )

        context.set_metadata(
            "portfolio_context",
            portfolio_context,
        )

    # =========================================================
    # AI Engine
    # =========================================================

    def _ai(
        self,
        context: PipelineContext,
    ) -> None:

        ai_context = AIContext(

            signal_strength=1.0,

            risk_score=0.20,

            performance_score=0.80,

            portfolio_score=0.90,

            optimization_score=0.75,

        )

        ai_decision = self.ai_engine.evaluate(
            ai_context,
        )

        if not ai_decision.approved:

            context.reject(
                decision="AI_ENGINE_FAILED",
                reason=ai_decision.reason,
            )

            return

        context.ai_result = ai_decision

        context.set_metadata(
            "ai_decision",
            ai_decision,
        )

    # =========================================================
    # Execution Engine
    # =========================================================

    def _execution(
        self,
        context: PipelineContext,
    ) -> None:

        execution_context = ExecutionContext(

            execution_id=context.pipeline_id,

            symbol=context.symbol,

            timeframe=context.timeframe,

            strategy_result=context.strategy_result,

            signal_result=context.signals,

            risk_result=context.risk_result,

            ai_result=context.ai_result,

        )

        execution_context = (
            self.execution_manager.execute(
                execution_context,
            )
        )

        if execution_context.failed:

            context.reject(
                decision="EXECUTION_ENGINE_FAILED",
                reason=execution_context.reason,
            )

            return

        # -------------------------------------------------
        # Execution Result
        # -------------------------------------------------

        context.execution_result = (
            execution_context.execution_result
        )

        # -------------------------------------------------
        # Preserve Full Execution Context
        # -------------------------------------------------

        context.set_metadata(
            "execution_context",
            execution_context,
        )

        # -------------------------------------------------
        # Propagate Trade Response
        #
        # ExecutionProcessor stores the MT5
        # TradeResponse inside ExecutionContext.
        #
        # Reporting operates on PipelineContext,
        # therefore the response must cross this
        # boundary.
        # -------------------------------------------------

        trade_response = (
            execution_context.metadata.get(
                "trade_response",
            )
        )

        if trade_response is not None:

            context.set_metadata(
                "trade_response",
                trade_response,
            )

        # -------------------------------------------------
        # Propagate MT5 Ticket
        # -------------------------------------------------

        mt5_ticket = (
            execution_context.metadata.get(
                "mt5_ticket",
            )
        )

        if mt5_ticket is not None:

            context.set_metadata(
                "mt5_ticket",
                mt5_ticket,
            )

        # -------------------------------------------------
        # Preserve Strategy Result
        # -------------------------------------------------

        context.set_metadata(
            "strategy_result",
            context.strategy_result,
        )

        # -------------------------------------------------
        # Complete Pipeline
        # -------------------------------------------------

        context.approve(
            decision="PIPELINE_COMPLETED",
            reason="Pipeline executed successfully.",
        )