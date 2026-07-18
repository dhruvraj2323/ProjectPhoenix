"""
Project Phoenix
Milestone M9 - Risk Management Engine

Module:
    risk_models.py

Purpose:
    Defines all core data models used by the Risk Management Engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional

from signals.signal_models import TradingSignal


class TradeDecision(Enum):
    """
    Final decision produced by the Risk Engine.
    """

    APPROVE = "APPROVE"
    REJECT = "REJECT"


@dataclass
class PositionSize:
    """
    Represents calculated position sizing.
    """

    quantity: float

    capital_allocated: float

    risk_percent: float


@dataclass
class StopLoss:
    """
    Represents stop-loss information.
    """

    price: float

    reason: str = ""


@dataclass
class TakeProfit:
    """
    Represents take-profit information.
    """

    price: float

    risk_reward_ratio: float = 2.0


@dataclass
class RiskContext:
    """
    Context required for risk calculations.
    """

    signal: TradingSignal

    account_balance: float

    symbol: str

    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RiskDecision:
    """
    Final output of the Risk Management Engine.
    """

    decision: TradeDecision

    position: PositionSize

    stop_loss: StopLoss

    take_profit: TakeProfit

    approved: bool

    reason: Optional[str] = None