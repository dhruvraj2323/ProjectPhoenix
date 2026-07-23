"""
=================================================
Project Phoenix
Signal Models
M34
=================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class SignalDirection(Enum):
    BUY = "BUY"
    SELL = "SELL"
    NEUTRAL = "NEUTRAL"


class SignalStrength(Enum):
    VERY_WEAK = 1
    WEAK = 2
    MODERATE = 3
    STRONG = 4
    VERY_STRONG = 5


class SignalStatus(Enum):
    CREATED = "CREATED"
    VALIDATED = "VALIDATED"
    REJECTED = "REJECTED"
    EXECUTED = "EXECUTED"


@dataclass(slots=True)
class TradingSignal:
    signal_id: str
    symbol: str
    timeframe: str

    direction: SignalDirection
    strength: SignalStrength

    confidence: float = 0.0

    created_at: datetime = field(
        default_factory=datetime.utcnow
    )

    metadata: dict[str, Any] = field(
        default_factory=dict
    )


@dataclass(slots=True)
class SignalStatistics:
    total_signals: int = 0
    buy_signals: int = 0
    sell_signals: int = 0
    rejected_signals: int = 0


@dataclass(slots=True)
class SignalResult:
    status: SignalStatus

    signals: list[TradingSignal] = field(
        default_factory=list
    )

    statistics: SignalStatistics = field(
        default_factory=SignalStatistics
    )

    message: str = ""