"""
Project Phoenix
Milestone M12 - Portfolio Management Engine

Module:
    portfolio_models.py

Purpose:
    Defines all core data models used by the
    Portfolio Management Engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class PositionDirection(Enum):
    """
    Direction of an open position.
    """

    BUY = "BUY"
    SELL = "SELL"


class PortfolioDecisionType(Enum):
    """
    Final decision produced by the
    Portfolio Engine.
    """

    APPROVE = "APPROVE"
    LIMIT_POSITION = "LIMIT_POSITION"
    REDUCE_POSITION = "REDUCE_POSITION"
    BLOCK_NEW_TRADE = "BLOCK_NEW_TRADE"
    EMERGENCY_EXIT = "EMERGENCY_EXIT"


@dataclass
class PositionInfo:
    """
    Represents one currently open position.
    """

    symbol: str
    direction: PositionDirection
    volume: float
    entry_price: float
    current_price: float
    floating_profit: float
    swap: float = 0.0
    commission: float = 0.0
    strategy: str = ""
    currency: str = "USD"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.symbol.strip():
            raise ValueError("Symbol cannot be empty.")

        if self.volume <= 0:
            raise ValueError("Volume must be greater than zero.")

        if self.entry_price <= 0:
            raise ValueError("Entry price must be greater than zero.")

        if self.current_price <= 0:
            raise ValueError("Current price must be greater than zero.")


@dataclass
class ExposureInfo:
    """
    Portfolio exposure information.
    """

    gross_exposure: float
    net_exposure: float
    long_exposure: float
    short_exposure: float

    symbol_exposure: Dict[str, float] = field(default_factory=dict)
    currency_exposure: Dict[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.gross_exposure < 0:
            raise ValueError("Gross exposure cannot be negative.")


@dataclass
class AllocationInfo:
    """
    Capital allocation summary.
    """

    capital_used: float
    capital_available: float
    allocation_percent: float
    risk_used: float
    risk_available: float

    def __post_init__(self) -> None:
        if self.capital_used < 0:
            raise ValueError("Capital used cannot be negative.")

        if self.capital_available < 0:
            raise ValueError("Capital available cannot be negative.")

        if not (0.0 <= self.allocation_percent <= 100.0):
            raise ValueError("Allocation percent must be between 0 and 100.")


@dataclass
class PortfolioRisk:
    """
    Portfolio risk summary.
    """

    risk_score: float
    drawdown: float
    margin_risk: float
    correlation_risk: float
    concentration_risk: float

    def __post_init__(self) -> None:
        if self.risk_score < 0:
            raise ValueError("Risk score cannot be negative.")


@dataclass
class PortfolioMetrics:
    """
    Overall portfolio metrics.
    """

    balance: float
    equity: float
    floating_profit: float
    floating_loss: float
    used_margin: float
    free_margin: float
    margin_level: float
    portfolio_heat: float
    open_positions: int
    daily_pnl: float
    weekly_pnl: float
    monthly_pnl: float

    def __post_init__(self) -> None:
        if self.balance <= 0:
            raise ValueError("Balance must be greater than zero.")

        if self.equity <= 0:
            raise ValueError("Equity must be greater than zero.")

        if self.open_positions < 0:
            raise ValueError("Open positions cannot be negative.")


@dataclass
class PortfolioLimits:
    """
    Configurable portfolio-level risk limits.
    """

    max_open_trades: int = 5
    max_drawdown_percent: float = 20.0
    max_exposure_percent: float = 300.0
    min_margin_level: float = 150.0
    max_correlation_percent: float = 85.0
    daily_loss_limit_percent: float = 5.0
    weekly_loss_limit_percent: float = 10.0
    monthly_loss_limit_percent: float = 15.0

    def __post_init__(self) -> None:
        if self.max_open_trades <= 0:
            raise ValueError("Maximum open trades must be greater than zero.")


@dataclass
class PortfolioContext:
    """
    Context supplied to the Portfolio Engine.
    """

    account_balance: float
    account_equity: float
    positions: List[PositionInfo]

    pending_orders: int = 0

    limits: PortfolioLimits = field(default_factory=PortfolioLimits)

    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.account_balance <= 0:
            raise ValueError("Account balance must be greater than zero.")

        if self.account_equity <= 0:
            raise ValueError("Account equity must be greater than zero.")

        if self.pending_orders < 0:
            raise ValueError("Pending orders cannot be negative.")


@dataclass
class PortfolioDecision:
    """
    Final output of the Portfolio Engine.
    """

    decision: PortfolioDecisionType
    metrics: PortfolioMetrics
    exposure: ExposureInfo
    allocation: AllocationInfo
    risk: PortfolioRisk
    approved: bool
    reason: Optional[str] = None

    def __post_init__(self) -> None:
        if self.approved and self.decision != PortfolioDecisionType.APPROVE:
            raise ValueError(
                "Approved portfolio decision must use APPROVE."
            )

        if (
            not self.approved
            and self.decision == PortfolioDecisionType.APPROVE
        ):
            raise ValueError(
                "Rejected portfolio decision cannot use APPROVE."
            )