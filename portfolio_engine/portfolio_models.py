"""
=================================================
Project Phoenix
Portfolio Models
M35
=================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum


class PositionStatus(Enum):
    """
    Position lifecycle.
    """

    OPEN = "OPEN"
    CLOSED = "CLOSED"


@dataclass(slots=True)
class PortfolioPosition:
    """
    Represents a single portfolio position.
    """

    trade_id: str

    symbol: str

    side: str

    quantity: float

    entry_price: float

    stop_loss: float

    take_profit: float

    current_price: float

    unrealized_pnl: float = 0.0

    realized_pnl: float = 0.0

    status: PositionStatus = PositionStatus.OPEN

    opened_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )

    closed_at: datetime | None = None


@dataclass(slots=True)
class PortfolioSummary:
    """
    Portfolio account summary.
    """

    balance: float = 10000.0

    equity: float = 10000.0

    free_margin: float = 10000.0

    used_margin: float = 0.0

    margin_level: float = 0.0

    floating_pnl: float = 0.0

    realized_pnl: float = 0.0

    total_trades: int = 0

    winning_trades: int = 0

    losing_trades: int = 0

    win_rate: float = 0.0

    updated_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )