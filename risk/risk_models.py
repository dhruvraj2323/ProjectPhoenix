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

    def __post_init__(self) -> None:
        if self.quantity <= 0:
            raise ValueError("Position quantity must be greater than zero.")

        if self.capital_allocated <= 0:
            raise ValueError("Capital allocated must be greater than zero.")

        if not (0.0 < self.risk_percent <= 100.0):
            raise ValueError("Risk percent must be between 0 and 100.")


@dataclass
class StopLoss:
    """
    Represents stop-loss information.
    """

    price: float
    reason: str = ""

    def __post_init__(self) -> None:
        if self.price <= 0:
            raise ValueError("Stop-loss price must be greater than zero.")


@dataclass
class TakeProfit:
    """
    Represents take-profit information.
    """

    price: float
    risk_reward_ratio: float = 2.0

    def __post_init__(self) -> None:
        if self.price <= 0:
            raise ValueError("Take-profit price must be greater than zero.")

        if self.risk_reward_ratio <= 0:
            raise ValueError("Risk-reward ratio must be greater than zero.")


@dataclass
class RiskContext:
    """
    Context required for risk calculations.
    """

    signal: TradingSignal
    account_balance: float
    symbol: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.account_balance <= 0:
            raise ValueError("Account balance must be greater than zero.")

        if not self.symbol.strip():
            raise ValueError("Symbol cannot be empty.")


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

    def __post_init__(self) -> None:
        if self.approved and self.decision != TradeDecision.APPROVE:
            raise ValueError(
                "Approved decision must use TradeDecision.APPROVE."
            )

        if not self.approved and self.decision != TradeDecision.REJECT:
            raise ValueError(
                "Rejected decision must use TradeDecision.REJECT."
            )