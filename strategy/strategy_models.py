"""
=================================================
Project Phoenix
Strategy Models
M53
=================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any


# =================================================
# Strategy Types
# =================================================


class StrategyType(Enum):
    """
    Supported trading strategies.
    """

    S01_EMA_TREND = "S01_EMA_TREND"

    S02_BREAKOUT_RETEST = "S02_BREAKOUT_RETEST"

    S03_PULLBACK = "S03_PULLBACK"

    S04_MEAN_REVERSION = "S04_MEAN_REVERSION"


# =================================================
# Trade Direction
# =================================================


class TradeDirection(Enum):
    """
    Trade direction.
    """

    BUY = "BUY"

    SELL = "SELL"

    NONE = "NONE"


# =================================================
# Strategy Status
# =================================================


class StrategyStatus(Enum):
    """
    Strategy execution status.
    """

    CREATED = "CREATED"

    APPROVED = "APPROVED"

    REJECTED = "REJECTED"

    EXECUTED = "EXECUTED"


# =================================================
# M53 Learning Mode
# =================================================


class LearningMode(Enum):
    """
    AI learning mode.
    """

    OFF = "OFF"

    LEARN = "LEARN"

    ASSIST = "ASSIST"


# =================================================
# AI Recommendation Type
# =================================================


class RecommendationType(Enum):
    """
    AI recommendation categories.
    """

    INCREASE_CONFIDENCE = (
        "INCREASE_CONFIDENCE"
    )

    REDUCE_CONFIDENCE = (
        "REDUCE_CONFIDENCE"
    )

    REJECT_TRADE = (
        "REJECT_TRADE"
    )

    ADJUST_PATTERN_WEIGHT = (
        "ADJUST_PATTERN_WEIGHT"
    )

    ADJUST_INDICATOR_WEIGHT = (
        "ADJUST_INDICATOR_WEIGHT"
    )

    ADJUST_TIMEFRAME_WEIGHT = (
        "ADJUST_TIMEFRAME_WEIGHT"
    )

    STRATEGY_IMPROVEMENT = (
        "STRATEGY_IMPROVEMENT"
    )

    NONE = "NONE"


# =================================================
# Multi-Timeframe Analysis
# =================================================


@dataclass(slots=True)
class TimeframeAnalysis:
    """
    Analysis for a single timeframe.
    """

    timeframe: str

    direction: TradeDirection = (
        TradeDirection.NONE
    )

    strategy_score: float = 0.0

    confidence: float = 0.0

    aligned: bool = False

    weight: float = 0.0

    reason: str = ""


# =================================================
# Multi-Timeframe Result
# =================================================


@dataclass(slots=True)
class MultiTimeframeResult:
    """
    Overall Multi-Timeframe result.
    """

    analyses: list[
        TimeframeAnalysis
    ] = field(
        default_factory=list,
    )

    alignment_score: float = 0.0

    overall_confidence: float = 0.0

    market_bias: TradeDirection = (
        TradeDirection.NONE
    )

    approved: bool = False

    reason: str = ""


# =================================================
# Strategy Signal
# =================================================


@dataclass(slots=True)
class StrategySignal:
    """
    Single strategy output.
    """

    strategy_id: str

    strategy_name: StrategyType

    direction: TradeDirection

    confidence: float

    entry_price: float

    stop_loss: float

    take_profit: float

    risk_percent: float

    reason: str

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )

    metadata: dict[
        str,
        Any,
    ] = field(
        default_factory=dict,
    )

    # -----------------------------------------
    # M51 Strategy Intelligence
    # -----------------------------------------

    strategy_score: float = 0.0

    pattern_score: float = 0.0

    indicator_score: float = 0.0

    confirmation_score: float = 0.0

    rank: int = 0

    selected: bool = False

    # -----------------------------------------
    # M52 Multi-Timeframe
    # -----------------------------------------

    timeframe: str = "M15"

    alignment_score: float = 0.0

    multi_timeframe_confirmed: bool = (
        False
    )

# =================================================
# Trade Snapshot
# =================================================


@dataclass(slots=True)
class TradeSnapshot:
    """
    Complete trade snapshot used
    for AI learning.
    """

    trade_id: str

    strategy_id: str

    symbol: str

    timeframe: str

    direction: TradeDirection

    entry_price: float

    exit_price: float = 0.0

    stop_loss: float = 0.0

    take_profit: float = 0.0

    pnl: float = 0.0

    win: bool = False

    strategy_score: float = 0.0

    ai_confidence: float = 0.0

    market_bias: TradeDirection = (
        TradeDirection.NONE
    )

    alignment_score: float = 0.0

    pattern_score: float = 0.0

    indicator_score: float = 0.0

    confirmation_score: float = 0.0

    metadata: dict[
        str,
        Any,
    ] = field(
        default_factory=dict,
    )

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )


# =================================================
# AI Recommendation
# =================================================


@dataclass(slots=True)
class AIRecommendation:
    """
    AI generated recommendation.
    """

    recommendation_type: (
        RecommendationType
    )

    confidence: float

    title: str

    description: str

    current_value: float = 0.0

    recommended_value: float = 0.0

    expected_improvement: float = 0.0

    approved: bool = False

    implemented: bool = False

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )

    metadata: dict[
        str,
        Any,
    ] = field(
        default_factory=dict,
    )


# =================================================
# Adaptive Weights
# =================================================


@dataclass(slots=True)
class AdaptiveWeights:
    """
    Adaptive statistical weights.
    """

    pattern_weight: float = 1.0

    indicator_weight: float = 1.0

    timeframe_weight: float = 1.0

    strategy_weight: float = 1.0

    confidence_weight: float = 1.0

    last_updated: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )


# =================================================
# AI Confidence Result
# =================================================


@dataclass(slots=True)
class AIConfidenceResult:
    """
    Final AI confidence calculation.
    """

    confidence: float = 0.0

    historical_similarity: float = 0.0

    pattern_success_rate: float = 0.0

    indicator_success_rate: float = 0.0

    timeframe_success_rate: float = 0.0

    market_regime_score: float = 0.0

    approved: bool = False

    reason: str = ""


# =================================================
# AI Learning Statistics
# =================================================


@dataclass(slots=True)
class AILearningStatistics:
    """
    AI learning statistics.
    """

    total_trades: int = 0

    winning_trades: int = 0

    losing_trades: int = 0

    breakeven_trades: int = 0

    win_rate: float = 0.0

    average_profit: float = 0.0

    average_loss: float = 0.0

    profit_factor: float = 0.0

    expectancy: float = 0.0

    last_learning_update: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )    

# =================================================
# Statistics
# =================================================


@dataclass(slots=True)
class StrategyStatistics:
    """
    Strategy evaluation statistics.
    """

    total_evaluated: int = 0

    approved: int = 0

    rejected: int = 0


# =================================================
# Strategy Result
# =================================================


@dataclass(slots=True)
class StrategyResult:
    """
    Complete Strategy Engine result.
    """

    status: StrategyStatus = (
        StrategyStatus.CREATED
    )

    selected_strategy: (
        StrategyType | None
    ) = None

    signals: list[
        StrategySignal
    ] = field(
        default_factory=list,
    )

    statistics: StrategyStatistics = field(
        default_factory=StrategyStatistics,
    )

    message: str = ""

    # -----------------------------------------
    # M51 Strategy Intelligence
    # -----------------------------------------

    best_score: float = 0.0

    selected_rank: int = 0

    selection_reason: str = ""

    evaluated_patterns: int = 0

    evaluated_indicators: int = 0

    # -----------------------------------------
    # M52 Multi-Timeframe
    # -----------------------------------------

    multi_timeframe_result: (
        MultiTimeframeResult
    ) = field(
        default_factory=MultiTimeframeResult,
    )

    # -----------------------------------------
    # M53 AI Decision Intelligence
    # -----------------------------------------

    learning_mode: LearningMode = (
        LearningMode.LEARN
    )

    ai_confidence_result: AIConfidenceResult = field(
        default_factory=AIConfidenceResult,
    )

    adaptive_weights: AdaptiveWeights = field(
        default_factory=AdaptiveWeights,
    )

    ai_learning_statistics: AILearningStatistics = field(
        default_factory=AILearningStatistics,
    )

    ai_recommendations: list[
        AIRecommendation
    ] = field(
        default_factory=list,
    )