"""
=================================================
Project Phoenix
Execution Models
M37
=================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class ExecutionOrder:
    """
    Execution order.
    """

    symbol: str
    side: str
    quantity: float
    price: float

    order_type: str = "MARKET"

    created_at: datetime = field(
        default_factory=datetime.utcnow,
    )


@dataclass(slots=True)
class ExecutionResult:
    """
    Execution result.
    """

    accepted: bool = False

    status: str = "PENDING"

    order_id: str = ""

    executed_price: float = 0.0

    reason: str = ""

    created_at: datetime = field(
        default_factory=datetime.utcnow,
    )