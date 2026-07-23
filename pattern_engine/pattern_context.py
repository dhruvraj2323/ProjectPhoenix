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

    engine_id: str

    symbol: str

    timeframe: str

    created_at: datetime = field(
        default_factory=datetime.utcnow
    )

    candles: list[dict[str, Any]] = field(
        default_factory=list
    )

    patterns: list[dict[str, Any]] = field(
        default_factory=list
    )

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    completed: bool = False

    failed: bool = False

    reason: str = ""

    def add_pattern(
        self,
        pattern: dict[str, Any],
    ) -> None:

        self.patterns.append(pattern)

    def get_patterns(
        self,
    ) -> list[dict[str, Any]]:

        return self.patterns

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

        self.patterns.clear()

        self.metadata.clear()

        self.completed = False

        self.failed = False

        self.reason = ""