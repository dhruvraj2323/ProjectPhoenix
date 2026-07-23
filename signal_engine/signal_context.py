"""
=================================================
Project Phoenix
Signal Context
M34
=================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class SignalContext:
    """
    Runtime context for Signal Engine.
    """

    engine_id: str
    symbol: str
    timeframe: str

    created_at: datetime = field(
        default_factory=datetime.utcnow
    )

    indicators: dict[str, Any] = field(
        default_factory=dict
    )

    patterns: list[dict[str, Any]] = field(
        default_factory=list
    )

    signals: list[dict[str, Any]] = field(
        default_factory=list
    )

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    completed: bool = False
    failed: bool = False
    reason: str = ""

    def add_signal(
        self,
        signal: dict[str, Any],
    ) -> None:

        self.signals.append(signal)

    def get_signal_count(
        self,
    ) -> int:

        return len(self.signals)

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
        self.completed = False
        self.failed = False
        self.reason = ""