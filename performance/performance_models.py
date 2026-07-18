"""
Project Phoenix
Milestone M11 - Performance Feedback Engine

Module:
    performance_models.py

Purpose:
    Defines all core data models used by the Performance Feedback Engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional


class TradeOutcome(Enum):
    """
    Final outcome of a completed trade.
    """

    WIN = "WIN"
    LOSS = "LOSS"
    BREAKEVEN = "BREAKEVEN"


class PerformanceDecisionType(Enum):
    """
    Final decision produced by the Performance Engine.
    """

    ACCEPT = "ACCEPT"
    REVIEW = "REVIEW"


@dataclass
class TradeResult:
    """
    Represents the result of a completed trade.
    """

    symbol: str

    outcome: TradeOutcome

    profit_loss: float

    entry_price: float

    exit_price: float

    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PerformanceMetrics:
    """
    Stores calculated performance statistics.
    """

    total_trades: int

    wins: int

    losses: int

    breakeven: int

    win_rate: float

    average_profit: float

    average_loss: float


@dataclass
class PerformanceContext:
    """
    Context required for performance analysis.
    """

    trades: list[TradeResult]

    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PerformanceDecision:
    """
    Final output of the Performance Engine.
    """

    decision: PerformanceDecisionType

    metrics: PerformanceMetrics

    approved: bool

    reason: Optional[str] = None