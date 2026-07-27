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

    created_at: datetime = field(
        default_factory=datetime.utcnow,
    )

    # --------------------------------------------------
    # Account Information
    # --------------------------------------------------

    account_id: str

    balance: float

    equity: float

    free_margin: float

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

    completed: bool = False

    failed: bool = False

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

    def mark_completed(
        self,
    ) -> None:
        """
        Mark execution completed.
        """

        self.completed = True

        self.failed = False

    def mark_failed(
        self,
        reason: str,
    ) -> None:
        """
        Mark execution failed.
        """

        self.completed = False

        self.failed = True

        self.reason = reason

    def reset(
        self,
    ) -> None:
        """
        Reset runtime state.
        """

        self.risk_result = RiskResult()

        self.metadata.clear()

        self.completed = False

        self.failed = False

        self.reason = ""