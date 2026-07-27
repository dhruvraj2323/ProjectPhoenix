"""
=================================================
Project Phoenix
Indicator Context
M32
=================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class IndicatorContext:
    """
    Shared runtime context for Indicator Engine.
    """

    # --------------------------------------------------
    # Engine Information
    # --------------------------------------------------

    engine_id: str

    created_at: datetime = field(
        default_factory=datetime.utcnow
    )

    # --------------------------------------------------
    # Market Information
    # --------------------------------------------------

    symbol: str = ""

    timeframe: str = ""

    # --------------------------------------------------
    # Input Data
    # --------------------------------------------------

    candles: list = field(
        default_factory=list
    )

    # --------------------------------------------------
    # Output Data
    # --------------------------------------------------

    indicators: dict[str, Any] = field(
        default_factory=dict
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

    def add_indicator(
        self,
        name: str,
        value: Any,
    ) -> None:
        """
        Store indicator result.
        """

        self.indicators[name] = value

    def get_indicator(
        self,
        name: str,
        default: Any = None,
    ) -> Any:
        """
        Retrieve indicator.
        """

        return self.indicators.get(
            name,
            default,
        )

    def set_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Store metadata.
        """

        self.metadata[key] = value

    def get_metadata(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Retrieve metadata.
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

    def mark_failed(
        self,
        reason: str,
    ) -> None:
        """
        Mark execution failed.
        """

        self.failed = True

        self.reason = reason

    def reset(
        self,
    ) -> None:
        """
        Reset runtime state.
        """

        self.indicators.clear()

        self.metadata.clear()

        self.completed = False

        self.failed = False

        self.reason = ""