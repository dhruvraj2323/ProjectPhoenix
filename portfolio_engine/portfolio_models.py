"""
=================================================
Project Phoenix
Portfolio Models
M35
=================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class PortfolioStatus(Enum):
    """
    Portfolio processing status.
    """

    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


@dataclass(slots=True)
class Position:
    """
    Single portfolio position.
    """

    symbol: str
    side: str
    volume: float
    entry_price: float
    current_price: float
    profit_loss: float = 0.0


@dataclass(slots=True)
class PortfolioStatistics:
    """
    Portfolio statistics.
    """

    total_positions: int = 0
    winning_positions: int = 0
    losing_positions: int = 0
    total_profit: float = 0.0
    total_loss: float = 0.0


@dataclass(slots=True)
class PortfolioSnapshot:
    """
    Portfolio snapshot.
    """

    account_id: str
    balance: float
    equity: float
    margin: float
    free_margin: float
    status: PortfolioStatus
    positions: list[Position] = field(default_factory=list)
    statistics: PortfolioStatistics = field(
        default_factory=PortfolioStatistics
    )
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(
        default_factory=datetime.utcnow
    )