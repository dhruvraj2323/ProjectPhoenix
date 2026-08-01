"""
=================================================
Project Phoenix
Strategy Models
M52
=================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
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
        default_factory=datetime.utcnow,
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