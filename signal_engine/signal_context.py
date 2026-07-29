"""
=================================================
Project Phoenix
Signal Context
M34
=================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import Any


@dataclass(slots=True)
class SignalContext:
    """
    Runtime context for Signal Engine.
    """

    # --------------------------------------------------
    # Engine Information
    # --------------------------------------------------

    engine_id: str

    # --------------------------------------------------
    # Market Information
    # --------------------------------------------------

    symbol: str

    timeframe: str

    # --------------------------------------------------
    # Runtime Information
    # --------------------------------------------------

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    # --------------------------------------------------
    # Input Data
    # --------------------------------------------------

    indicators: dict[str, Any] = field(
        default_factory=dict
    )

    patterns: list[dict[str, Any]] = field(
        default_factory=list
    )

    # --------------------------------------------------
    # Output Data
    # --------------------------------------------------

    signals: list[dict[str, Any]] = field(
        default_factory=list
    )

    # --------------------------------------------------
    # Runtime Metadata
    # --------------------------------------------------

    metadata: dict[str, Any] = field(
        default_factory=dict
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

    def add_signal(
        self,
        signal: dict[str, Any],
    ) -> None:

        self.signals.append(signal)

    def get_signal_count(
        self,
    ) -> int:

        return len(self.signals)

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

    def mark_completed(
        self,
    ) -> None:

        self.completed = True

    def mark_failed(
        self,
        reason: str,
    ) -> None:

        self.failed = True
        self.reason = reason

    def reset(
        self,
    ) -> None:

        self.signals.clear()
        self.metadata.clear()

        self.completed = False
        self.failed = False
        self.reason = ""