"""
=================================================
Project Phoenix
Strategy AI Models
M53
=================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

from strategy.strategy_models import (
    TradeDirection,
)


# =================================================
# AI Decision
# =================================================


class AIDecision(Enum):
    """
    Final AI decision.
    """

    APPROVE = "APPROVE"

    REVIEW = "REVIEW"

    REJECT = "REJECT"


# =================================================
# AI Memory Type
# =================================================


class AIMemoryType(Enum):
    """
    AI memory classification.
    """

    SHORT_TERM = "SHORT_TERM"

    MEDIUM_TERM = "MEDIUM_TERM"

    LONG_TERM = "LONG_TERM"


# =================================================
# AI Learning Status
# =================================================


class AILearningStatus(Enum):
    """
    Learning execution state.
    """

    PENDING = "PENDING"

    LEARNED = "LEARNED"

    FAILED = "FAILED"


# =================================================
# AI Trade Similarity
# =================================================


@dataclass(slots=True)
class AITradeSimilarity:
    """
    Historical similarity
    between trades.
    """

    trade_id: str

    similarity_score: float

    historical_win_rate: float

    confidence: float

    matched_patterns: int

    matched_indicators: int

    matched_timeframes: int

    direction: TradeDirection

    reason: str = ""

    metadata: dict[
        str,
        Any,
    ] = field(
        default_factory=dict,
    )

# =================================================
# AI Learning Record
# =================================================


@dataclass(slots=True)
class AILearningRecord:
    """
    Single AI learning record.
    """

    learning_id: str

    trade_id: str

    strategy_id: str

    symbol: str

    timeframe: str

    direction: TradeDirection

    learning_status: (
        AILearningStatus
    ) = (
        AILearningStatus.PENDING
    )

    similarity_score: float = 0.0

    confidence_before: float = 0.0

    confidence_after: float = 0.0

    pnl: float = 0.0

    win: bool = False

    notes: str = ""

    created_at: datetime = field(
        default_factory=datetime.utcnow,
    )

    metadata: dict[
        str,
        Any,
    ] = field(
        default_factory=dict,
    )


# =================================================
# AI Memory Summary
# =================================================


@dataclass(slots=True)
class AIMemorySummary:
    """
    AI memory statistics.
    """

    memory_type: AIMemoryType

    total_records: int = 0

    winning_records: int = 0

    losing_records: int = 0

    average_similarity: float = 0.0

    average_confidence: float = 0.0

    average_profit: float = 0.0

    win_rate: float = 0.0

    last_updated: datetime = field(
        default_factory=datetime.utcnow,
    )

    metadata: dict[
        str,
        Any,
    ] = field(
        default_factory=dict,
    )

# =================================================
# AI Weight Update
# =================================================


@dataclass(slots=True)
class AIWeightUpdate:
    """
    Proposed adaptive weight update.

    These values are recommendations only.
    Strategy logic is never modified
    automatically.
    """

    update_id: str

    pattern_weight: float = 1.0

    indicator_weight: float = 1.0

    timeframe_weight: float = 1.0

    strategy_weight: float = 1.0

    confidence_weight: float = 1.0

    expected_improvement: float = 0.0

    approved: bool = False

    implemented: bool = False

    created_at: datetime = field(
        default_factory=datetime.utcnow,
    )

    metadata: dict[
        str,
        Any,
    ] = field(
        default_factory=dict,
    )


# =================================================
# AI Learning Report
# =================================================


@dataclass(slots=True)
class AILearningReport:
    """
    Complete AI learning report.
    """

    report_id: str

    generated_at: datetime = field(
        default_factory=datetime.utcnow,
    )

    decision: AIDecision = (
        AIDecision.REVIEW
    )

    total_records: int = 0

    winning_trades: int = 0

    losing_trades: int = 0

    win_rate: float = 0.0

    average_similarity: float = 0.0

    average_confidence: float = 0.0

    expected_improvement: float = 0.0

    recommendations: list[
        AIWeightUpdate
    ] = field(
        default_factory=list,
    )

    summary: AIMemorySummary | None = None

    notes: str = ""

    metadata: dict[
        str,
        Any,
    ] = field(
        default_factory=dict,
    )    