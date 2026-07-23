"""
=================================================
Project Phoenix
Pattern Models
M33
=================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class PatternStatus(Enum):
    """
    Pattern Engine execution status.
    """

    CREATED = "CREATED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


@dataclass(slots=True)
class PatternSignal:
    """
    Single detected candlestick pattern.
    """

    name: str
    index: int
    bullish: bool
    bearish: bool
    strength: float
    metadata: dict[str, Any] = field(
        default_factory=dict
    )


@dataclass(slots=True)
class PatternStatistics:
    """
    Pattern Engine statistics.
    """

    total_patterns: int = 0
    bullish_patterns: int = 0
    bearish_patterns: int = 0


@dataclass(slots=True)
class PatternResult:
    """
    Complete Pattern Engine result.
    """

    engine_id: str
    symbol: str
    timeframe: str

    status: PatternStatus

    created_at: datetime = field(
        default_factory=datetime.utcnow
    )

    patterns: list[PatternSignal] = field(
        default_factory=list
    )

    statistics: PatternStatistics = field(
        default_factory=PatternStatistics
    )