"""
=================================================
Project Phoenix
Strategy AI Learning
M53
=================================================
"""

from __future__ import annotations

from strategy.strategy_ai_memory import (
    StrategyAIMemory,
)

from strategy.strategy_ai_models import (
    AILearningReport,
    AILearningRecord,
    AIWeightUpdate,
    AIMemoryType,
)

from strategy.strategy_models import (
    TradeSnapshot,
)


class StrategyAILearning:
    """
    AI Learning Engine.

    Responsibilities

    • Analyze historical trades

    • Learn from outcomes

    • Generate AI recommendations

    • Generate adaptive weight proposals

    • Produce learning reports

    This module never changes
    strategy logic automatically.
    """

    def __init__(
        self,
        memory: StrategyAIMemory,
    ) -> None:

        self.memory = memory

    # --------------------------------------------------
    # Main Learning Entry
    # --------------------------------------------------

    def learn(
        self,
    ) -> AILearningReport:
        """
        Execute complete
        AI learning cycle.
        """

        summary = (
            self.memory.build_memory_summary(
                AIMemoryType.LONG_TERM,
            )
        )

        report = AILearningReport(

            report_id=(
                "AI-LEARNING-001"
            ),

            summary=summary,

            total_records=(
                summary.total_records
            ),

            winning_trades=(
                summary.winning_records
            ),

            losing_trades=(
                summary.losing_records
            ),

            win_rate=(
                summary.win_rate
            ),

            average_confidence=(
                summary.average_confidence
            ),

            average_similarity=(
                summary.average_similarity
            ),

        )

        self.analyze_trades(
            report,
        )

        return report

    # --------------------------------------------------
    # Trade Analysis
    # --------------------------------------------------

    def analyze_trades(
        self,
        report: AILearningReport,
    ) -> None:
        """
        Analyze all stored trades.
        """

        trades = (
            self.memory.get_all_trades()
        )

        if not trades:

            report.notes = (
                "No historical trades."
            )

            return

        profitable = sum(

            1

            for trade in trades

            if trade.pnl > 0

        )

        report.notes = (

            f"Analyzed "

            f"{len(trades)} trades "

            f"({profitable} profitable)."

        )

    # --------------------------------------------------
    # Pattern Analysis
    # --------------------------------------------------

    def analyze_patterns(
        self,
        report: AILearningReport,
    ) -> None:
        """
        Analyze historical
        pattern performance.
        """

        summary = report.summary

        if summary is None:

            return

        if summary.win_rate >= 70.0:

            report.notes += (
                " Pattern performance is strong."
            )

        elif summary.win_rate < 40.0:

            report.notes += (
                " Pattern performance needs improvement."
            )

    # --------------------------------------------------
    # Indicator Analysis
    # --------------------------------------------------

    def analyze_indicators(
        self,
        report: AILearningReport,
    ) -> None:
        """
        Analyze indicator
        performance.
        """

        summary = report.summary

        if summary is None:

            return

        if summary.average_confidence >= 80.0:

            report.notes += (
                " Indicator confidence is excellent."
            )

        elif summary.average_confidence < 50.0:

            report.notes += (
                " Indicator confidence is weak."
            )

    # --------------------------------------------------
    # Timeframe Analysis
    # --------------------------------------------------

    def analyze_timeframes(
        self,
        report: AILearningReport,
    ) -> None:
        """
        Analyze timeframe
        performance.
        """

        summary = report.summary

        if summary is None:

            return

        if summary.total_records >= 100:

            report.notes += (
                " Sufficient historical timeframe data."
            )

        else:

            report.notes += (
                " Timeframe history is limited."
            )

    # --------------------------------------------------
    # Weight Proposal
    # --------------------------------------------------

    def generate_weight_updates(
        self,
        report: AILearningReport,
    ) -> None:
        """
        Generate adaptive
        weight proposals.

        Recommendations only.
        """

        summary = report.summary

        if summary is None:

            return

        update = AIWeightUpdate(

            update_id="WU-001",

            expected_improvement=0.0,

        )

        if summary.win_rate >= 70.0:

            update.pattern_weight = 1.10

            update.indicator_weight = 1.05

            update.timeframe_weight = 1.05

            update.expected_improvement = 3.0

        elif summary.win_rate <= 40.0:

            update.pattern_weight = 0.90

            update.indicator_weight = 0.95

            update.timeframe_weight = 0.95

            update.expected_improvement = 5.0

        else:

            update.expected_improvement = 1.0

        report.recommendations.append(
            update,
        )

    # --------------------------------------------------
    # Recommendation Generator
    # --------------------------------------------------

    def generate_recommendations(
        self,
        report: AILearningReport,
    ) -> None:
        """
        Generate learning
        recommendations.
        """

        summary = report.summary

        if summary is None:

            return

        if summary.win_rate >= 70.0:

            report.notes += (
                " AI recommends maintaining the "
                "current strategy configuration."
            )

        elif summary.win_rate >= 50.0:

            report.notes += (
                " AI recommends reviewing "
                "pattern quality and entries."
            )

        else:

            report.notes += (
                " AI recommends detailed "
                "strategy optimization."
            )

    # --------------------------------------------------
    # Learning Report Builder
    # --------------------------------------------------

    def build_learning_report(
        self,
    ) -> AILearningReport:
        """
        Build complete
        AI learning report.
        """

        report = self.learn()

        self.analyze_patterns(
            report,
        )

        self.analyze_indicators(
            report,
        )

        self.analyze_timeframes(
            report,
        )

        self.generate_weight_updates(
            report,
        )

        self.generate_recommendations(
            report,
        )

        return report

    # --------------------------------------------------
    # Utility Methods
    # --------------------------------------------------

    def total_trades(
        self,
    ) -> int:
        """
        Return total trades
        available for learning.
        """

        return self.memory.total_trades

    def total_learning_records(
        self,
    ) -> int:
        """
        Return total learning
        records.
        """

        return (
            self.memory.total_learning_records
        )

    def reset_learning(
        self,
    ) -> None:
        """
        Reset AI memory.
        """

        self.memory.reset()                