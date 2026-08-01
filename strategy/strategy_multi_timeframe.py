"""
=================================================
Project Phoenix
Strategy Multi-Timeframe
M52
=================================================
"""

from __future__ import annotations

from strategy.strategy_models import (
    MultiTimeframeResult,
    TimeframeAnalysis,
    TradeDirection,
)


class StrategyMultiTimeframe:
    """
    Calculates Multi-Timeframe
    intelligence.

    Responsible only for
    timeframe confirmation.

    It never creates signals.
    """

    # -----------------------------------------
    # Frozen Timeframe Weights
    # -----------------------------------------

    WEIGHTS = {

        "D1": 30.0,

        "H4": 25.0,

        "H1": 20.0,

        "M15": 15.0,

        "M5": 7.0,

        "M1": 3.0,

    }

    # -----------------------------------------
    # Master Calculator
    # -----------------------------------------

    def evaluate(
        self,
        analyses: list[
            TimeframeAnalysis
        ],
    ) -> MultiTimeframeResult:
        """
        Calculate complete
        Multi-Timeframe result.
        """

        result = (
            MultiTimeframeResult()
        )

        result.analyses = analyses

        if not analyses:

            result.reason = (
                "No timeframe analysis."
            )

            return result

        buy_weight = 0.0

        sell_weight = 0.0

        total_confidence = 0.0

        # -----------------------------------------
        # Calculate Weighted Bias
        # -----------------------------------------

        for analysis in analyses:

            weight = self.WEIGHTS.get(
                analysis.timeframe,
                0.0,
            )

            analysis.weight = weight

            total_confidence += (
                analysis.confidence
            )

            if (
                analysis.direction
                == TradeDirection.BUY
            ):

                buy_weight += weight

            elif (
                analysis.direction
                == TradeDirection.SELL
            ):

                sell_weight += weight

        # -----------------------------------------
        # Determine Market Bias
        # -----------------------------------------

        if buy_weight > sell_weight:

            result.market_bias = (
                TradeDirection.BUY
            )

            alignment = buy_weight

        elif sell_weight > buy_weight:

            result.market_bias = (
                TradeDirection.SELL
            )

            alignment = sell_weight

        else:

            result.market_bias = (
                TradeDirection.NONE
            )

            alignment = 0.0

        # -----------------------------------------
        # Final Scores
        # -----------------------------------------

        result.alignment_score = round(
            alignment,
            2,
        )

        result.overall_confidence = round(

            total_confidence

            /

            len(
                analyses,
            ),

            2,

        )

        # -----------------------------------------
        # Approval Logic
        # -----------------------------------------

        if alignment >= 70.0:

            result.approved = True

            result.reason = (

                "Multi-timeframe confirmation passed."

            )

        else:

            result.approved = False

            result.reason = (

                "Multi-timeframe confirmation failed."

            )

        return result

    # --------------------------------------------------
    # Helper
    # --------------------------------------------------

    def default_analysis(
        self,
        timeframe: str,
    ) -> TimeframeAnalysis:
        """
        Create default timeframe analysis.
        """

        return TimeframeAnalysis(

            timeframe=timeframe,

            direction=TradeDirection.NONE,

            strategy_score=0.0,

            confidence=0.0,

            aligned=False,

            weight=self.WEIGHTS.get(
                timeframe,
                0.0,
            ),

            reason="",

        )    