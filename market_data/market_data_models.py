"""
=================================================
Project Phoenix
Market Data Models
M40.X.1
=================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class MarketDataResult:
    """
    Standard output of the Market Data Engine.

    This object is passed through the pipeline instead
    of exposing internal Market Data modules.
    """

    success: bool = False

    candles: list[dict[str, Any]] = field(default_factory=list)

    validation_report: dict[str, Any] = field(default_factory=dict)

    timeframe: str = "M1"

    candle_count: int = 0

    errors: list[str] = field(default_factory=list)

    def add_error(self, message: str) -> None:
        """
        Add an error message.
        """
        self.errors.append(message)

    @property
    def has_errors(self) -> bool:
        """
        True if one or more errors exist.
        """
        return len(self.errors) > 0