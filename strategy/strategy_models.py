"""
=================================================
Project Phoenix
Strategy Models
M38
=================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class StrategyType(Enum):
    """
    Supported trading strategies.
    """

    S01_EMA_TREND = "S01_EMA_TREND"
    S02_BREAKOUT_RETEST = "S02_BREAKOUT_RETEST"
    S03_PULLBACK = "S03_PULLBACK"
    S04_MEAN_REVERSION = "S04_MEAN_REVERSION"


class TradeDirection(Enum):
    """
    Trade direction.
    """

    BUY = "BUY"
    SELL = "SELL"
    NONE = "NONE"


class StrategyStatus(Enum):
    """
    Strategy execution status.
    """

    CREATED = "CREATED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    EXECUTED = "EXECUTED"


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

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    # -----------------------------------------
    # Strategy Intelligence (M51)
    # -----------------------------------------

    strategy_score: float = 0.0

    pattern_score: float = 0.0

    indicator_score: float = 0.0

    confirmation_score: float = 0.0

    rank: int = 0

    selected: bool = False

@dataclass(slots=True)
class StrategyStatistics:
    """
    Strategy evaluation statistics.
    """

    total_evaluated: int = 0

    approved: int = 0

    rejected: int = 0


@dataclass(slots=True)
class StrategyResult:
    """
    Complete Strategy Engine result.
    """

    status: StrategyStatus = StrategyStatus.CREATED

    selected_strategy: StrategyType | None = None

    signals: list[StrategySignal] = field(
        default_factory=list,
    )

    statistics: StrategyStatistics = field(
        default_factory=StrategyStatistics,
    )

    message: str = ""

    # -----------------------------------------
    # Strategy Intelligence (M51)
    # -----------------------------------------

    best_score: float = 0.0

    selected_rank: int = 0

    selection_reason: str = ""

    evaluated_patterns: int = 0

    evaluated_indicators: int = 0    