"""
=================================================
Project Phoenix
Execution Models
M37
=================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum


class ExecutionStatus(Enum):
    """
    Execution status.
    """

    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    EXECUTED = "EXECUTED"


@dataclass(slots=True)
class ExecutionOrder:
    """
    Trade execution request.
    """

    strategy_id: str

    symbol: str

    side: str

    quantity: float

    entry_price: float

    stop_loss: float

    take_profit: float

    risk_percent: float

    order_type: str = "MARKET"

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )


@dataclass(slots=True)
class ExecutionResult:
    """
    Final execution result.
    """

    accepted: bool = False

    status: ExecutionStatus = (
        ExecutionStatus.PENDING
    )

    order_id: str = ""

    executed_price: float = 0.0

    reason: str = ""

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )