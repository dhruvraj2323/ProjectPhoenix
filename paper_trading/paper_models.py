"""
=================================================
Project Phoenix
Paper Trading Models
M24
=================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum


class PaperPositionStatus(Enum):
    """
    Paper position lifecycle.
    """

    OPEN = "OPEN"
    CLOSED = "CLOSED"


@dataclass(slots=True)
class PaperOrder:
    """
    Virtual order created by Execution Engine.
    """

    strategy_id: str

    symbol: str

    side: str

    quantity: float

    entry_price: float

    stop_loss: float

    take_profit: float

    risk_percent: float

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )


@dataclass(slots=True)
class PaperPosition:
    """
    Virtual open position.
    """

    ticket: int

    strategy_id: str

    symbol: str

    side: str

    quantity: float

    entry_price: float

    current_price: float

    stop_loss: float

    take_profit: float

    unrealized_pnl: float = 0.0

    realized_pnl: float = 0.0

    status: PaperPositionStatus = (
        PaperPositionStatus.OPEN
    )

    opened_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )

    closed_at: datetime | None = None


@dataclass(slots=True)
class PaperPortfolio:
    """
    Virtual trading account.
    """

    balance: float = 10000.0

    equity: float = 10000.0

    free_margin: float = 10000.0

    used_margin: float = 0.0

    floating_pnl: float = 0.0

    realized_pnl: float = 0.0

    total_positions: int = 0

    total_closed_positions: int = 0

    updated_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )


@dataclass(slots=True)
class PaperTradingStatus:
    """
    Runtime state.
    """

    running: bool = False

    virtual_balance: float = 10000.0

    total_positions: int = 0


@dataclass(slots=True)
class PaperTradingResult:
    """
    Processing result.
    """

    approved: bool = False

    reason: str = ""

    status: PaperTradingStatus = field(
        default_factory=PaperTradingStatus,
    )