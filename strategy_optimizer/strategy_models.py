"""
Project Phoenix
Milestone M13 - Strategy Optimizer Engine

Module:
    strategy_models.py

Purpose:
    Defines all core data models used by the
    Strategy Optimizer Engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class OptimizationType(Enum):
    """
    Type of optimization recommendation.
    """

    NONE = "NONE"

    EMA_PERIOD = "EMA_PERIOD"

    RSI_PERIOD = "RSI_PERIOD"

    RISK_PERCENT = "RISK_PERCENT"

    SIGNAL_STRENGTH = "SIGNAL_STRENGTH"

    CONFIDENCE_THRESHOLD = "CONFIDENCE_THRESHOLD"


class OptimizationStatus(Enum):
    """
    Status of optimization.
    """

    APPROVED = "APPROVED"

    REJECTED = "REJECTED"

    REVIEW_REQUIRED = "REVIEW_REQUIRED"


@dataclass
class StrategyPerformance:
    """
    Performance summary used by the optimizer.
    """

    total_trades: int

    win_rate: float

    average_profit: float

    average_loss: float

    drawdown: float

    profit_factor: float

    sharpe_ratio: float

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )


@dataclass
class OptimizationRecommendation:
    """
    Recommended strategy adjustment.
    """

    optimization_type: OptimizationType

    current_value: float

    suggested_value: float

    reason: str

    confidence: float


@dataclass
class StrategyContext:
    """
    Context supplied to the optimizer.
    """

    performance: StrategyPerformance

    current_parameters: Dict[str, float]

    optimization_history: List[str] = field(
        default_factory=list
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )


@dataclass
class OptimizationDecision:
    """
    Final output of the Strategy Optimizer Engine.
    """

    status: OptimizationStatus

    recommendation: OptimizationRecommendation

    approved: bool

    reason: Optional[str] = None