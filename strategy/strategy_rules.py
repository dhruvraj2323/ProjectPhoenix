"""
=================================================
Project Phoenix
Strategy Rules
M51
=================================================
"""

from __future__ import annotations

from strategy.strategy_context import (
    StrategyContext,
)

from strategy.strategy_models import (
    StrategyStatus,
    StrategyType,
    TradeDirection,
)

from strategy.strategy_scoring import (
    StrategyScoring,
)

from strategy.strategy_signal_builder import (
    StrategySignalBuilder,
)

from strategy.strategy_multi_timeframe import (
    StrategyMultiTimeframe,
)

from strategy.strategy_timeframe_ranker import (
    StrategyTimeframeRanker,
)

from strategy.strategy_models import (
    TimeframeAnalysis,
)


class StrategyRules:
    """
    Implements all trading strategies.

    Responsibilities

    • Evaluate strategies

    • Calculate intelligence

    • Build strategy signals

    • Select approved strategy
    """

    def __init__(self) -> None:

        self.scoring = StrategyScoring()

        self.builder = StrategySignalBuilder()

        self.multi_timeframe = (
            StrategyMultiTimeframe()
        )

        self.ranker = (
            StrategyTimeframeRanker()
        )

    # --------------------------------------------------
    # Internal Helper
    # --------------------------------------------------

    def _apply_signal(
        self,
        context: StrategyContext,
        signal,
    ) -> None:
        """
        Apply approved strategy signal.
        """

        signal.rank = 1

        signal.selected = True

        context.strategy_result.signals.append(
            signal,
        )

        context.strategy_result.selected_strategy = (
            signal.strategy_name
        )

        context.strategy_result.status = (
            StrategyStatus.APPROVED
        )

        context.strategy_result.best_score = (
            signal.strategy_score
        )

        context.strategy_result.selected_rank = 1

        context.strategy_result.selection_reason = (
            signal.reason
        )

        context.strategy_result.statistics.total_evaluated += 1

        context.strategy_result.statistics.approved += 1

        # --------------------------------------------------
    # M52
    # Build Timeframe Analysis
    # --------------------------------------------------

    def _build_timeframe_analysis(
        self,
        signal,
    ) -> list[
        TimeframeAnalysis
    ]:
        """
        Build default timeframe
        analyses for M52.

        Actual values will be
        replaced once true
        multi-timeframe data
        becomes available.
        """

        analyses = []

        for timeframe in (

            "D1",

            "H4",

            "H1",

            "M15",

            "M5",

            "M1",

        ):

            analyses.append(

                TimeframeAnalysis(

                    timeframe=timeframe,

                    direction=signal.direction,

                    strategy_score=signal.strategy_score,

                    confidence=signal.confidence,

                    aligned=True,

                )

            )

        return analyses

    # --------------------------------------------------
    # M52
    # Store Multi-Timeframe Result
    # --------------------------------------------------

    def _apply_multi_timeframe(
        self,
        context: StrategyContext,
        signal,
    ) -> None:
        """
        Execute Multi-Timeframe
        confirmation.
        """

        analyses = self._build_timeframe_analysis(
            signal,
        )

        result = self.multi_timeframe.evaluate(
            analyses,
        )

        context.multi_timeframe_result = result

        context.strategy_result.multi_timeframe_result = (
            result
        )

        signal.alignment_score = (
            result.alignment_score
        )

        signal.multi_timeframe_confirmed = (
            result.approved
        )                

    # --------------------------------------------------
    # S01
    # --------------------------------------------------

    def evaluate_s01(
        self,
        context: StrategyContext,
    ) -> StrategyContext:
        """
        EMA Trend Strategy
        """

        scores = self.scoring.calculate(
            context,
        )

        ema9 = context.indicators.get(
            "EMA9",
            0.0,
        )

        ema21 = context.indicators.get(
            "EMA21",
            0.0,
        )

        ema200 = context.indicators.get(
            "EMA200",
            0.0,
        )

        rsi14 = context.indicators.get(
            "RSI14",
            0.0,
        )

        price = context.market_data.get(
            "price",
            0.0,
        )

        breakout = any(

            pattern.get(
                "name",
            ) == "BREAKOUT"

            for pattern in context.patterns

        )

        retest = any(

            pattern.get(
                "name",
            ) in (

                "BULLISH_RETEST",

                "BEARISH_RETEST",

            )

            for pattern in context.patterns

        )

        signal = None

        # ------------------------------------
        # M52 Multi-Timeframe
        # ------------------------------------

        multi_result = None

        # ---------------- BUY ----------------

        if (

            price > ema200

            and ema9 > ema21

            and rsi14 > 55

        ):

            signal = self.builder.build(

                strategy_id="S01",

                strategy_name=StrategyType.S01_EMA_TREND,

                direction=TradeDirection.BUY,

                entry_price=price,

                stop_loss=0.0,

                take_profit=0.0,

                risk_percent=1.0,

                reason="EMA Trend BUY confirmed.",

                strategy_score=scores.strategy_score,

                pattern_score=scores.pattern_score,

                indicator_score=scores.indicator_score,

                confirmation_score=scores.confirmation_score,

                confidence=scores.confidence,

            )

        # ---------------- SELL ----------------

        elif (

            price < ema200

            and ema9 < ema21

            and rsi14 < 45


        ):

            signal = self.builder.build(

                strategy_id="S01",

                strategy_name=StrategyType.S01_EMA_TREND,

                direction=TradeDirection.SELL,

                entry_price=price,

                stop_loss=0.0,

                take_profit=0.0,

                risk_percent=1.0,

                reason="EMA Trend SELL confirmed.",

                strategy_score=scores.strategy_score,

                pattern_score=scores.pattern_score,

                indicator_score=scores.indicator_score,

                confirmation_score=scores.confirmation_score,

                confidence=scores.confidence,

            )

        if signal is not None:

            self._apply_multi_timeframe(
                context,
                signal,
            )

            self._apply_signal(

                context,

                signal,

            )

        else:

            context.strategy_result.statistics.total_evaluated += 1

            context.strategy_result.statistics.rejected += 1

        return context

    # --------------------------------------------------
    # S02
    # --------------------------------------------------

    def evaluate_s02(
        self,
        context: StrategyContext,
    ) -> StrategyContext:
        """
        Breakout + Retest Strategy.

        Reserved for M52.
        """

        return context

    # --------------------------------------------------
    # S03
    # --------------------------------------------------

    def evaluate_s03(
        self,
        context: StrategyContext,
    ) -> StrategyContext:
        """
        Pullback Strategy.

        Reserved for M52.
        """

        return context

    # --------------------------------------------------
    # S04
    # --------------------------------------------------

    def evaluate_s04(
        self,
        context: StrategyContext,
    ) -> StrategyContext:
        """
        Mean Reversion Strategy.

        Reserved for M52.
        """

        return context        