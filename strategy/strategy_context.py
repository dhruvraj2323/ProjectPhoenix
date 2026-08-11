"""
=================================================
Project Phoenix
Strategy Context
M52
=================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from strategy.strategy_models import (
    StrategyResult,
    MultiTimeframeResult,
    TradeDirection,
    LearningMode,
    TradeSnapshot,
    AIRecommendation,
    AdaptiveWeights,
    AIConfidenceResult,
    AILearningStatistics,
)

@dataclass(slots=True)
class StrategyContext:
    """
    Shared runtime context for Strategy Engine.
    """

    # --------------------------------------------------
    # Engine Information
    # --------------------------------------------------

    engine_id: str

    symbol: str

    timeframe: str

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )

    # --------------------------------------------------
    # Input Data
    # --------------------------------------------------

    indicators: dict[str, Any] = field(
        default_factory=dict,
    )

    patterns: list[dict[str, Any]] = field(
        default_factory=list,
    )

    market_data: dict[str, Any] = field(
        default_factory=dict,
    )

    # --------------------------------------------------
    # M51 Strategy Intelligence
    # --------------------------------------------------

    pattern_score: float = 0.0

    indicator_score: float = 0.0

    confirmation_score: float = 0.0

    strategy_score: float = 0.0

    selected_strategy_rank: int = 0

    # --------------------------------------------------
    # M52 Multi-Timeframe Intelligence
    # --------------------------------------------------

    primary_timeframe: str = "M15"

    execution_timeframe: str = "M1"

    entry_timeframe: str = "M5"

    trend_timeframe: str = "H1"

    major_trend_timeframe: str = "H4"

    market_bias_timeframe: str = "D1"

    alignment_score: float = 0.0

    multi_timeframe_score: float = 0.0

    market_bias: TradeDirection = (
        TradeDirection.NONE
    )

    timeframe_scores: dict[
        str,
        float,
    ] = field(
        default_factory=dict,
    )

    # --------------------------------------------------
    # Strategy Result
    # --------------------------------------------------

    strategy_result: StrategyResult = field(
        default_factory=StrategyResult,
    )

    multi_timeframe_result: MultiTimeframeResult = field(
        default_factory=MultiTimeframeResult,
    )

    # --------------------------------------------------
    # M53 AI Runtime
    # --------------------------------------------------

    learning_mode: LearningMode = (
        LearningMode.LEARN
    )

    trade_snapshot: (
        TradeSnapshot | None
    ) = None

    ai_confidence_result: AIConfidenceResult = field(
        default_factory=AIConfidenceResult,
    )

    adaptive_weights: AdaptiveWeights = field(
        default_factory=AdaptiveWeights,
    )

    ai_recommendations: list[
        AIRecommendation
    ] = field(
        default_factory=list,
    )

    ai_learning_statistics: AILearningStatistics = field(
        default_factory=AILearningStatistics,
    )

    # --------------------------------------------------
    # Metadata
    # --------------------------------------------------

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    strategy_candidates: list[
        dict[str, Any]
    ] = field(
        default_factory=list,
    )

    # --------------------------------------------------
    # Runtime State
    # --------------------------------------------------

    completed: bool = False

    failed: bool = False

    reason: str = ""

    # --------------------------------------------------
    # Utility Methods
    # --------------------------------------------------

    def complete(
        self,
    ) -> None:

        self.completed = True

        self.failed = False

    def fail(
        self,
        reason: str,
    ) -> None:

        self.completed = False

        self.failed = True

        self.reason = reason

    def reset(
        self,
    ) -> None:

        self.strategy_result = (
            StrategyResult()
        )

        self.multi_timeframe_result = (
            MultiTimeframeResult()
        )

        self.trade_snapshot = None

        self.ai_confidence_result = (
            AIConfidenceResult()
        )

        self.adaptive_weights = (
            AdaptiveWeights()
        )

        self.ai_learning_statistics = (
            AILearningStatistics()
        )

        self.ai_recommendations.clear()

        self.learning_mode = (
            LearningMode.LEARN
        )

        self.metadata.clear()

        self.pattern_score = 0.0

        self.indicator_score = 0.0

        self.confirmation_score = 0.0

        self.strategy_score = 0.0

        self.alignment_score = 0.0

        self.multi_timeframe_score = 0.0

        self.market_bias = (
            TradeDirection.NONE
        )

        self.selected_strategy_rank = 0

        self.timeframe_scores.clear()

        self.strategy_candidates.clear()

        self.completed = False

        self.failed = False

        self.reason = ""

    # --------------------------------------------------
    # M53 AI Helpers
    # --------------------------------------------------

    def add_ai_recommendation(
        self,
        recommendation: AIRecommendation,
    ) -> None:
        """
        Store AI recommendation.
        """

        self.ai_recommendations.append(
            recommendation,
        )

    def set_trade_snapshot(
        self,
        snapshot: TradeSnapshot,
    ) -> None:
        """
        Store current trade snapshot.
        """

        self.trade_snapshot = snapshot

    def set_ai_confidence(
        self,
        result: AIConfidenceResult,
    ) -> None:
        """
        Store AI confidence result.
        """

        self.ai_confidence_result = result

    def set_learning_mode(
        self,
        mode: LearningMode,
    ) -> None:
        """
        Change AI learning mode.
        """

        self.learning_mode = mode        