"""
=================================================
Project Phoenix
Strategy Engine
M52
=================================================
"""

from __future__ import annotations

from strategy.strategy_context import (
    StrategyContext,
)

from strategy.strategy_logger import (
    StrategyLogger,
)

from strategy.strategy_rules import (
    StrategyRules,
)

from strategy.strategy_validator import (
    StrategyValidator,
)

from strategy.strategy_ai_engine import (
    StrategyAIEngine,
)

from strategy.strategy_models import (
    TradeSnapshot,
)


class StrategyEngine:
    """
    Executes the complete
    Strategy Engine pipeline.

    M52 Pipeline

    Validate
        ↓
    Strategy Evaluation
        ↓
    Multi-Timeframe Intelligence
        ↓
    Finalize
    """

    def __init__(
        self,
    ) -> None:

        self.validator = (
            StrategyValidator()
        )

        self.rules = (
            StrategyRules()
        )

        self.logger = (
            StrategyLogger()
        )

        self.ai_engine = (
            StrategyAIEngine()
        )

    # --------------------------------------------------
    # Trade Snapshot Builder
    # --------------------------------------------------

    def _build_trade_snapshot(
        self,
        context: StrategyContext,
    ) -> None:
        """
        Build trade snapshot for
        AI learning.
        """

        if (
            not context.strategy_result.signals
        ):
            return

        signal = (
            context.strategy_result.signals[0]
        )

        snapshot = TradeSnapshot(

            trade_id=(
                context.engine_id
            ),

            strategy_id=(
                signal.strategy_id
            ),

            symbol=(
                context.symbol
            ),

            timeframe=(
                context.timeframe
            ),

            direction=(
                signal.direction
            ),

            entry_price=(
                signal.entry_price
            ),

            strategy_score=(
                signal.strategy_score
            ),

            ai_confidence=(
                signal.confidence
            ),

            market_bias=(
                signal.direction
            ),

            alignment_score=(
                signal.alignment_score
            ),

            pattern_score=(
                signal.pattern_score
            ),

            indicator_score=(
                signal.indicator_score
            ),

        )

        context.set_trade_snapshot(
            snapshot,
        )
    
    # --------------------------------------------------
    # Run Engine
    # --------------------------------------------------

    def run(
        self,
        context: StrategyContext,
    ) -> StrategyContext:
        """
        Execute complete
        Strategy Engine.
        """

        # ------------------------------------
        # Start
        # ------------------------------------

        self.logger.log_start(
            context,
        )

        # ------------------------------------
        # Validate
        # ------------------------------------

        if not self.validator.validate(
            context,
        ):

            self.logger.log_failure(
                context,
            )

            return context

        # ------------------------------------
        # Evaluate Strategies
        # ------------------------------------

        context = self.rules.evaluate_s01(
            context,
        )

        context = self.rules.evaluate_s02(
            context,
        )

        context = self.rules.evaluate_s03(
            context,
        )

        context = self.rules.evaluate_s04(
            context,
        )

        # ------------------------------------
        # Build Trade Snapshot
        # ------------------------------------

        self._build_trade_snapshot(
            context,
        )

        # ------------------------------------
        # AI Assisted Intelligence
        # ------------------------------------

        if self.ai_engine.is_ready():

            context = self.ai_engine.run(
                context,
            )

        # --------------------------------------------------
        # AI Diagnostics
        # --------------------------------------------------

        def ai_status(
            self,
        ) -> dict[
            str,
            object,
        ]:
            """
            Return current AI engine status.
            """

            return self.ai_engine.diagnostics()

        # ------------------------------------
        # Store AI Statistics
        # ------------------------------------

        if (
            context.ai_confidence_result
            is not None
        ):

            context.metadata[
                "ai_confidence"
            ] = (
                context.ai_confidence_result.confidence
            )

            context.metadata[
                "ai_approved"
            ] = (
                context.ai_confidence_result.approved
            )

            context.metadata[
                "ai_confidence_level"
            ] = (
                self.ai_engine
                .confidence
                .confidence_level(
                    context.ai_confidence_result.confidence
                )
            )        

        # ------------------------------------
        # Complete
        # ------------------------------------

        context.complete()

        # ------------------------------------
        # Finish
        # ------------------------------------

        self.logger.log_finish(
            context,
        )

        return context