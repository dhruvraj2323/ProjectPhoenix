"""
=================================================
Project Phoenix
Strategy Rules
M38
=================================================
"""

from __future__ import annotations

from strategy.strategy_context import (
    StrategyContext,
)

from strategy.strategy_models import (
    StrategySignal,
    StrategyType,
    StrategyStatus,
    TradeDirection,
)


class StrategyRules:
    """
    Implements all trading strategies.
    """

    # --------------------------------------------------
    # S01 EMA Trend Strategy
    # --------------------------------------------------

    def evaluate_s01(
        self,
        context: StrategyContext,
    ) -> StrategyContext:

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

        signal = None

        # ---------------- BUY ----------------

        if (

            price > ema200

            and ema9 > ema21

            and rsi14 > 55

        ):

            signal = StrategySignal(

                strategy_id="S01",

                strategy_name=StrategyType.S01_EMA_TREND,

                direction=TradeDirection.BUY,

                confidence=90.0,

                entry_price=price,

                stop_loss=0.0,

                take_profit=0.0,

                risk_percent=1.0,

                reason=(
                    "EMA Trend BUY confirmed."
                ),

            )

        # ---------------- SELL ----------------

        elif (

            price < ema200

            and ema9 < ema21

            and rsi14 < 45

        ):

            signal = StrategySignal(

                strategy_id="S01",

                strategy_name=StrategyType.S01_EMA_TREND,

                direction=TradeDirection.SELL,

                confidence=90.0,

                entry_price=price,

                stop_loss=0.0,

                take_profit=0.0,

                risk_percent=1.0,

                reason=(
                    "EMA Trend SELL confirmed."
                ),

            )

        if signal is not None:

            context.strategy_result.signals.append(
                signal
            )

            context.strategy_result.selected_strategy = (
                StrategyType.S01_EMA_TREND
            )

            context.strategy_result.status = (
                StrategyStatus.APPROVED
            )

            context.strategy_result.statistics.total_evaluated += 1

            context.strategy_result.statistics.approved += 1

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

        return context

    # --------------------------------------------------
    # S03
    # --------------------------------------------------

    def evaluate_s03(
        self,
        context: StrategyContext,
    ) -> StrategyContext:

        return context

    # --------------------------------------------------
    # S04
    # --------------------------------------------------

    def evaluate_s04(
        self,
        context: StrategyContext,
    ) -> StrategyContext:

        return context