"""
=================================================
Project Phoenix
Strategy AI Engine
M53
=================================================
"""

from __future__ import annotations

from strategy.strategy_ai_confidence import (
    StrategyAIConfidence,
)

from strategy.strategy_ai_learning import (
    StrategyAILearning,
)

from strategy.strategy_ai_memory import (
    StrategyAIMemory,
)

from strategy.strategy_context import (
    StrategyContext,
)


class StrategyAIEngine:
    """
    Central AI orchestrator.

    Responsibilities

    • Store completed trades

    • Execute learning

    • Calculate confidence

    • Update strategy context

    This module never executes
    trading strategies directly.
    """

    def __init__(
        self,
    ) -> None:

        self.memory = (
            StrategyAIMemory()
        )

        self.learning = (
            StrategyAILearning(
                self.memory,
            )
        )

        self.confidence = (
            StrategyAIConfidence(
                self.learning,
            )
        )

    # --------------------------------------------------
    # Main AI Pipeline
    # --------------------------------------------------

    def run(
        self,
        context: StrategyContext,
    ) -> StrategyContext:
        """
        Execute complete
        AI pipeline.
        """

        if context.trade_snapshot is not None:

            self.memory.add_trade(

                context.trade_snapshot,

            )

        learning_report = (

            self.learning.build_learning_report()

        )

        confidence = (

            self.confidence.build_confidence_result()

        )

        context.ai_learning_statistics.total_trades = (

            learning_report.total_records

        )

        context.ai_learning_statistics.winning_trades = (

            learning_report.winning_trades

        )

        context.ai_learning_statistics.losing_trades = (

            learning_report.losing_trades

        )

        context.set_ai_confidence(

            confidence,

        )

        return context

    # --------------------------------------------------
    # Memory Operations
    # --------------------------------------------------

    def add_trade(
        self,
        context: StrategyContext,
    ) -> None:
        """
        Store trade snapshot
        into AI memory.
        """

        if context.trade_snapshot is None:

            return

        self.memory.add_trade(

            context.trade_snapshot,

        )

    def total_trades(
        self,
    ) -> int:
        """
        Return total trades
        stored in AI memory.
        """

        return self.memory.total_trades

    # --------------------------------------------------
    # Learning Operations
    # --------------------------------------------------

    def learning_report(
        self,
    ):
        """
        Return latest
        AI learning report.
        """

        return (

            self.learning.build_learning_report()

        )

    # --------------------------------------------------
    # Confidence Operations
    # --------------------------------------------------

    def confidence_result(
        self,
    ):
        """
        Return latest
        AI confidence result.
        """

        return (

            self.confidence.build_confidence_result()

        )

    # --------------------------------------------------
    # Runtime Information
    # --------------------------------------------------

    def ai_status(
        self,
    ) -> dict[
        str,
        object,
    ]:
        """
        Return AI runtime status.
        """

        return {

            "memory_trades": (

                self.memory.total_trades

            ),

            "learning_records": (

                self.memory.total_learning_records

            ),

            "engine_ready": True,

        }

    # --------------------------------------------------
    # Engine State
    # --------------------------------------------------

    def initialize(
        self,
    ) -> None:
        """
        Initialize AI engine.

        Reserved for future startup
        operations such as loading
        persisted AI memory.
        """

        return None

    def is_ready(
        self,
    ) -> bool:
        """
        Check whether the
        AI engine is ready.
        """

        return (

            self.memory is not None

            and

            self.learning is not None

            and

            self.confidence is not None

        )

    # --------------------------------------------------
    # Reset
    # --------------------------------------------------

    def reset(
        self,
    ) -> None:
        """
        Reset complete
        AI engine.
        """

        self.memory.reset()

    # --------------------------------------------------
    # Diagnostics
    # --------------------------------------------------

    def diagnostics(
        self,
    ) -> dict[
        str,
        object,
    ]:
        """
        Return AI diagnostics.
        """

        return {

            "ready": self.is_ready(),

            "memory_trades": (

                self.memory.total_trades

            ),

            "learning_records": (

                self.memory.total_learning_records

            ),

            "confidence_available": True,

            "learning_available": True,

            "memory_available": True,

        }                