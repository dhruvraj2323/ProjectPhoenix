"""
=================================================
Project Phoenix
Risk Context
M36
=================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from risk_engine.risk_models import (
    RiskResult,
)


@dataclass(slots=True)
class RiskContext:
    """
    Shared runtime context for Risk Engine.
    """

    # --------------------------------------------------
    # Engine Information
    # --------------------------------------------------

    engine_id: str

    # --------------------------------------------------
    # Account Information
    # --------------------------------------------------

    account_id: str

    balance: float

    equity: float

    free_margin: float

    # --------------------------------------------------
    # Runtime Information
    # --------------------------------------------------

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )

    # --------------------------------------------------
    # Output Data
    # --------------------------------------------------

    risk_result: RiskResult = field(
        default_factory=RiskResult,
    )

    # --------------------------------------------------
    # Runtime Metadata
    # --------------------------------------------------

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    # --------------------------------------------------
    # Execution State
    # --------------------------------------------------

    approved: bool = False

    completed: bool = False

    failed: bool = False

    decision: str = ""

    reason: str = ""

    # --------------------------------------------------
    # Utility Methods
    # --------------------------------------------------

    def set_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Store runtime metadata.
        """

        self.metadata[key] = value

    def get_metadata(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Retrieve runtime metadata.
        """

        return self.metadata.get(
            key,
            default,
        )

    # --------------------------------------------------
    # Execution Status
    # --------------------------------------------------

    def approve(
        self,
        decision: str,
        reason: str,
    ) -> None:
        """
        Mark successful execution.
        """

        self.approved = True
        self.completed = True
        self.failed = False

        self.decision = decision
        self.reason = reason

    def reject(
        self,
        decision: str,
        reason: str,
    ) -> None:
        """
        Mark failed execution.
        """

        self.approved = False
        self.completed = True
        self.failed = True

        self.decision = decision
        self.reason = reason

    # --------------------------------------------------
    # Reset
    # --------------------------------------------------

    def reset(
        self,
    ) -> None:
        """
        Reset runtime state.
        """

        self.risk_result = RiskResult()

        self.metadata.clear()

        self.approved = False

        self.completed = False

        self.failed = False

        self.decision = ""

        self.reason = ""