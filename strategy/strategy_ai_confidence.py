"""
=================================================
Project Phoenix
Strategy AI Confidence
M53
=================================================
"""

from __future__ import annotations

from strategy.strategy_ai_learning import (
    StrategyAILearning,
)

from strategy.strategy_ai_models import (
    AILearningReport,
)

from strategy.strategy_models import (
    AIConfidenceResult,
)


class StrategyAIConfidence:
    """
    AI Confidence Engine.

    Responsibilities

    • Calculate AI confidence

    • Analyze historical learning

    • Produce AIConfidenceResult

    This module never performs
    learning or modifies strategy logic.
    """

    def __init__(
        self,
        learning: StrategyAILearning,
    ) -> None:

        self.learning = learning

    # --------------------------------------------------
    # Main Calculator
    # --------------------------------------------------

    def calculate(
        self,
    ) -> AIConfidenceResult:
        """
        Execute complete
        confidence calculation.
        """

        report = (
            self.learning.build_learning_report()
        )

        result = AIConfidenceResult()

        result.historical_similarity = (
            self.confidence_from_history(
                report,
            )
        )

        result.pattern_success_rate = (
            self.confidence_from_patterns(
                report,
            )
        )

        return result

    # --------------------------------------------------
    # Historical Confidence
    # --------------------------------------------------

    def confidence_from_history(
        self,
        report: AILearningReport,
    ) -> float:
        """
        Historical confidence.

        Weight:
        25%
        """

        return round(

            report.win_rate,

            2,

        )

    # --------------------------------------------------
    # Similarity Confidence
    # --------------------------------------------------

    def confidence_from_similarity(
        self,
        report: AILearningReport,
    ) -> float:
        """
        Historical similarity.

        Weight:
        20%
        """

        return round(

            report.average_similarity,

            2,

        )

    # --------------------------------------------------
    # Pattern Confidence
    # --------------------------------------------------

    def confidence_from_patterns(
        self,
        report: AILearningReport,
    ) -> float:
        """
        Pattern success.

        Weight:
        15%
        """

        return round(

            report.win_rate,

            2,

        )

    # --------------------------------------------------
    # Indicator Confidence
    # --------------------------------------------------

    def confidence_from_indicators(
        self,
        report: AILearningReport,
    ) -> float:
        """
        Indicator success.

        Weight:
        15%
        """

        return round(

            report.average_confidence,

            2,

        )

    # --------------------------------------------------
    # Timeframe Confidence
    # --------------------------------------------------

    def confidence_from_timeframes(
        self,
        report: AILearningReport,
    ) -> float:
        """
        Timeframe success.

        Weight:
        10%
        """

        if report.total_records >= 500:

            return 100.0

        if report.total_records >= 100:

            return 80.0

        if report.total_records >= 50:

            return 65.0

        return 50.0

    # --------------------------------------------------
    # Alignment Confidence
    # --------------------------------------------------

    def confidence_from_alignment(
        self,
        report: AILearningReport,
    ) -> float:
        """
        Multi-timeframe alignment.

        Weight:
        10%
        """

        if report.win_rate >= 70.0:

            return 90.0

        if report.win_rate >= 50.0:

            return 75.0

        return 55.0

    # --------------------------------------------------
    # Market Regime Confidence
    # --------------------------------------------------

    def confidence_from_market_regime(
        self,
        report: AILearningReport,
    ) -> float:
        """
        Market regime confidence.

        Weight:
        5%

        Reserved for future
        market regime engine.
        """

        return 50.0

    # --------------------------------------------------
    # Final Confidence
    # --------------------------------------------------

    def build_confidence_result(
        self,
    ) -> AIConfidenceResult:
        """
        Build complete
        AI confidence result.
        """

        report = (
            self.learning.build_learning_report()
        )

        history = self.confidence_from_history(
            report,
        )

        similarity = (
            self.confidence_from_similarity(
                report,
            )
        )

        patterns = (
            self.confidence_from_patterns(
                report,
            )
        )

        indicators = (
            self.confidence_from_indicators(
                report,
            )
        )

        timeframes = (
            self.confidence_from_timeframes(
                report,
            )
        )

        alignment = (
            self.confidence_from_alignment(
                report,
            )
        )

        regime = (
            self.confidence_from_market_regime(
                report,
            )
        )

        confidence = (

            history * 0.25

            +

            similarity * 0.20

            +

            patterns * 0.15

            +

            indicators * 0.15

            +

            timeframes * 0.10

            +

            alignment * 0.10

            +

            regime * 0.05

        )

        result = AIConfidenceResult(

            confidence=round(
                confidence,
                2,
            ),

            historical_similarity=round(
                similarity,
                2,
            ),

            pattern_success_rate=round(
                patterns,
                2,
            ),

            indicator_success_rate=round(
                indicators,
                2,
            ),

            timeframe_success_rate=round(
                timeframes,
                2,
            ),

            market_regime_score=round(
                regime,
                2,
            ),

            approved=(
                confidence >= 70.0
            ),

            reason=(
                "AI confidence calculated "
                "using weighted historical analysis."
            ),

        )

        return result

    # --------------------------------------------------
    # Utility Methods
    # --------------------------------------------------

    def confidence_level(
        self,
        confidence: float,
    ) -> str:
        """
        Return confidence level.
        """

        if confidence >= 95.0:

            return (
                "EXTREMELY_HIGH"
            )

        if confidence >= 85.0:

            return "HIGH"

        if confidence >= 70.0:

            return "MEDIUM"

        if confidence >= 55.0:

            return "WEAK"

        return "VERY_WEAK"

    def reset(
        self,
    ) -> None:
        """
        Reset confidence engine.

        Reserved for future cache
        implementations.
        """

        return None                