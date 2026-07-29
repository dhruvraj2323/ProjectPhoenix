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
from typing import Any

from execution_engine.execution_models import (
    ExecutionOrder,
    ExecutionResult,
)


@dataclass(slots=True)
class ExecutionContext:
    """
    Runtime context for Execution Engine.
    """

    # --------------------------------------------------
    # Engine Information
    # --------------------------------------------------

    execution_id: str

    symbol: str

    timeframe: str

    created_at: datetime = field(
        default_factory=datetime.utcnow,
    )

    # --------------------------------------------------
    # Previous Engine Results
    # --------------------------------------------------

    strategy_result: Any = None

    signal_result: Any = None

    risk_result: Any = None

    ai_result: Any = None

    # --------------------------------------------------
    # Execution
    # --------------------------------------------------

    order: ExecutionOrder | None = None

    execution_result: ExecutionResult = field(
        default_factory=ExecutionResult,
    )

    # --------------------------------------------------
    # Metadata
    # --------------------------------------------------

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    # --------------------------------------------------
    # Runtime State
    # --------------------------------------------------

    completed: bool = False

    failed: bool = False

    reason: str = ""

    # --------------------------------------------------
    # Utility Methods
    # --------------------------------------------------

    def complete(self) -> None:

        self.completed = True

        self.failed = False

    def fail(
        self,
        reason: str,
    ) -> None:

        self.completed = False

        self.failed = True

        self.reason = reason

    def reset(self) -> None:

        self.order = None

        self.execution_result = ExecutionResult()

        self.metadata.clear()

        self.completed = False

        self.failed = False

        self.reason = ""