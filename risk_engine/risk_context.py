"""
=================================================
Project Phoenix
Risk Context
M36
=================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from risk_engine.risk_models import (
    RiskResult,
)


@dataclass(slots=True)
class RiskContext:
    """
    Shared context for Risk Engine.
    """

    engine_id: str

    account_id: str

    balance: float

    equity: float

    free_margin: float

    created_at: datetime = field(
        default_factory=datetime.utcnow,
    )

    risk_result: RiskResult = field(
        default_factory=RiskResult,
    )

    metadata: dict = field(
        default_factory=dict,
    )

    completed: bool = False

    failed: bool = False

    reason: str = ""

    def complete(self) -> None:
        """
        Mark execution completed.
        """

        self.completed = True

        self.failed = False

    def fail(
        self,
        reason: str,
    ) -> None:
        """
        Mark execution failed.
        """

        self.completed = False

        self.failed = True

        self.reason = reason