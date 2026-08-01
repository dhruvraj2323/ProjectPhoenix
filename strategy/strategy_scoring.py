"""
=================================================
Project Phoenix
Strategy Scoring
M51
=================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from strategy.strategy_context import (
    StrategyContext,
)


# =================================================
# Strategy Score
# =================================================


@dataclass(slots=True)
class StrategyScore:
    """
    Final strategy intelligence scores.
    """

    pattern_score: float = 0.0

    indicator_score: float = 0.0

    confirmation_score: float = 0.0

    strategy_score: float = 0.0

    confidence: float = 0.0


# =================================================
# Strategy Scoring
# =================================================


class StrategyScoring:
    """
    Strategy Intelligence Calculator.

    Responsible only for scoring.

    It never creates signals.

    It never decides BUY or SELL.
    """

    # --------------------------------------------------
    # Master Calculator
    # --------------------------------------------------

    def calculate(
        self,
        context: StrategyContext,
    ) -> StrategyScore:
        """
        Calculate complete strategy
        intelligence.
        """

        pattern_score = (
            self.calculate_pattern_score(
                context.patterns,
            )
        )

        indicator_score = (
            self.calculate_indicator_score(
                context.indicators,
            )
        )

        confirmation_score = (
            self.calculate_confirmation_score(
                context.patterns,
            )
        )

        strategy_score = (
            self.calculate_strategy_score(
                pattern_score,
                indicator_score,
                confirmation_score,
            )
        )

        confidence = (
            self.calculate_confidence(
                strategy_score,
            )
        )

        context.pattern_score = (
            pattern_score
        )

        context.indicator_score = (
            indicator_score
        )

        context.confirmation_score = (
            confirmation_score
        )

        context.strategy_score = (
            strategy_score
        )

        return StrategyScore(

            pattern_score=pattern_score,

            indicator_score=indicator_score,

            confirmation_score=confirmation_score,

            strategy_score=strategy_score,

            confidence=confidence,

        )

    # --------------------------------------------------
    # Pattern Score
    # --------------------------------------------------

    def calculate_pattern_score(
        self,
        patterns: list[
            dict[str, Any]
        ],
    ) -> float:
        """
        Calculate total pattern score.
        """

        if not patterns:

            return 0.0

        score = 0.0

        for pattern in patterns:

            strength = pattern.get(
                "strength",
                0.0,
            )

            score += strength

            if pattern.get(
                "confirmed",
                False,
            ):

                score += 2.0

            name = pattern.get(
                "name",
                "",
            )

            if name in (

                "BREAKOUT",

                "BREAKDOWN",

            ):

                score += 3.0

            if name in (

                "BULLISH_RETEST",

                "BEARISH_RETEST",

            ):

                score += 2.0

        return round(
            score,
            3,
        )

    # --------------------------------------------------
    # Indicator Score
    # --------------------------------------------------

    def calculate_indicator_score(
        self,
        indicators: dict[
            str,
            Any,
        ],
    ) -> float:
        """
        Calculate indicator score.
        """

        score = 0.0

        ema9 = indicators.get(
            "EMA9",
            0.0,
        )

        ema21 = indicators.get(
            "EMA21",
            0.0,
        )

        ema200 = indicators.get(
            "EMA200",
            0.0,
        )

        if ema9 > ema21:

            score += 20.0

        if ema21 > ema200:

            score += 20.0

        rsi14 = indicators.get(
            "RSI14",
            50.0,
        )

        if 40 <= rsi14 <= 70:

            score += 20.0

        macd = indicators.get(
            "MACD",
            {},
        )

        if isinstance(
            macd,
            dict,
        ):

            macd_line = macd.get(
                "macd",
                0.0,
            )

            signal_line = macd.get(
                "signal",
                0.0,
            )

            if macd_line > signal_line:

                score += 15.0

        supertrend = indicators.get(
            "SUPERTREND",
            False,
        )

        if supertrend:

            score += 15.0

        price = indicators.get(
            "PRICE",
            0.0,
        )

        vwap = indicators.get(
            "VWAP",
            0.0,
        )

        if (

            vwap > 0.0

            and

            price > vwap

        ):

            score += 10.0

        atr = indicators.get(
            "ATR",
            0.0,
        )

        if atr > 0.0:

            score += 5.0

        return round(
            score,
            3,
        )

    # --------------------------------------------------
    # Confirmation Score
    # --------------------------------------------------

    def calculate_confirmation_score(
        self,
        patterns: list[
            dict[str, Any]
        ],
    ) -> float:
        """
        Calculate confirmation score.
        """

        score = 0.0

        for pattern in patterns:

            if pattern.get(
                "confirmed",
                False,
            ):

                score += pattern.get(
                    "confirmation_score",
                    0.0,
                )

        return round(
            score,
            3,
        )

    # --------------------------------------------------
    # Strategy Score
    # --------------------------------------------------

    def calculate_strategy_score(
        self,
        pattern_score: float,
        indicator_score: float,
        confirmation_score: float,
    ) -> float:
        """
        Overall strategy score.
        """

        score = (

            pattern_score

            +

            indicator_score

            +

            confirmation_score

        )

        return round(
            score,
            3,
        )

    # --------------------------------------------------
    # Confidence
    # --------------------------------------------------

    def calculate_confidence(
        self,
        strategy_score: float,
    ) -> float:
        """
        Convert strategy score
        into confidence.
        """

        confidence = min(

            100.0,

            50.0 + strategy_score,

        )

        return round(
            confidence,
            2,
        )

    # --------------------------------------------------
    # Future Extension Hooks
    # --------------------------------------------------

    def calculate_multi_timeframe_score(
        self,
    ) -> float:
        """
        Reserved for M52.
        """

        return 0.0

    def calculate_ai_score(
        self,
    ) -> float:
        """
        Reserved for M53.
        """

        return 0.0

    def calculate_market_regime_score(
        self,
    ) -> float:
        """
        Reserved for M53.
        """

        return 0.0            