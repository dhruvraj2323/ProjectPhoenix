"""
=================================================
Project Phoenix
Pattern Context
M33
=================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class PatternContext:
    """
    Runtime context for Pattern Engine.
    """

    # --------------------------------------------------
    # Engine Information
    # --------------------------------------------------

    engine_id: str

    symbol: str

    timeframe: str

    created_at: datetime = field(
        default_factory=datetime.utcnow
    )

    # --------------------------------------------------
    # Market Data
    # --------------------------------------------------

    candles: list[dict[str, Any]] = field(
        default_factory=list
    )

    # --------------------------------------------------
    # Pattern Results
    # --------------------------------------------------

    patterns: list[dict[str, Any]] = field(
        default_factory=list
    )

    # --------------------------------------------------
    # Runtime Metadata
    # --------------------------------------------------

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    # --------------------------------------------------
    # Engine State
    # --------------------------------------------------

    approved: bool = False

    completed: bool = False

    failed: bool = False

    decision: str = ""

    reason: str = ""

    # --------------------------------------------------
    # Pattern Management
    # --------------------------------------------------

    def add_pattern(
        self,
        pattern: dict[str, Any],
    ) -> None:

        self.patterns.append(pattern)

    def get_patterns(
        self,
    ) -> list[dict[str, Any]]:

        return self.patterns

    # --------------------------------------------------
    # Metadata
    # --------------------------------------------------

    def set_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:

        self.metadata[key] = value

    def get_metadata(
        self,
        key: str,
        default: Any = None,
    ) -> Any:

        return self.metadata.get(
            key,
            default,
        )

    # --------------------------------------------------
    # Engine Status
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
        self.completed = False
        self.failed = True

        self.decision = decision
        self.reason = reason

    # --------------------------------------------------
    # Reset
    # --------------------------------------------------

    def reset(
        self,
    ) -> None:

        self.patterns.clear()

        self.metadata.clear()

        self.approved = False

        self.completed = False

        self.failed = False

        self.decision = ""

        self.reason = ""