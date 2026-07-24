"""
=================================================
Project Phoenix
Execution Context
M37
=================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from execution_engine.execution_models import (
    ExecutionOrder,
    ExecutionResult,
)


@dataclass(slots=True)
class ExecutionContext:
    """
    Runtime execution context.
    """

    execution_id: str

    symbol: str

    signal: str

    quantity: float

    price: float

    created_at: datetime = field(
        default_factory=datetime.utcnow,
    )

    order: ExecutionOrder | None = None

    execution_result: ExecutionResult = field(
        default_factory=ExecutionResult,
    )

    metadata: dict = field(
        default_factory=dict,
    )

    completed: bool = False

    failed: bool = False

    reason: str = ""