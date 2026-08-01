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