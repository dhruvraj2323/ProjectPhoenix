"""
=================================================
Project Phoenix
Trading Context
M39
=================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class TradingContext:
    """
    Master runtime context shared across
    the complete trading workflow.
    """

    # --------------------------------------------------
    # Session Information
    # --------------------------------------------------

    trading_id: str

    created_at: datetime = field(
        default_factory=datetime.utcnow
    )

    # --------------------------------------------------
    # Market Information
    # --------------------------------------------------

    symbol: str = ""

    timeframe: str = ""

    # --------------------------------------------------
    # Pipeline Data
    # --------------------------------------------------

    candles: list = field(
        default_factory=list
    )

    indicators: dict[str, Any] = field(
        default_factory=dict
    )

    patterns: dict[str, Any] = field(
        default_factory=dict
    )

    # --------------------------------------------------
    # Strategy
    # --------------------------------------------------

    strategy_name: str = ""

    signal: str = ""

    signal_strength: float = 0.0

    # --------------------------------------------------
    # Risk
    # --------------------------------------------------

    risk_score: float = 0.0

    risk_passed: bool = False

    # --------------------------------------------------
    # AI Decision
    # --------------------------------------------------

    ai_score: float = 0.0

    ai_confidence: float = 0.0

    ai_decision: str = ""

    # --------------------------------------------------
    # Execution
    # --------------------------------------------------

    order_id: str = ""

    execution_price: float = 0.0

    quantity: float = 0.0

    # --------------------------------------------------
    # Runtime Metadata
    # --------------------------------------------------

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    # --------------------------------------------------
    # Final Status
    # --------------------------------------------------

    approved: bool = False

    rejected: bool = False

    decision: str = ""

    reason: str = ""

    # --------------------------------------------------
    # Indicator Methods
    # --------------------------------------------------

    def add_indicator(
        self,
        name: str,
        value: Any,
    ) -> None:

        self.indicators[name] = value

    def get_indicator(
        self,
        name: str,
        default: Any = None,
    ) -> Any:

        return self.indicators.get(
            name,
            default,
        )

    # --------------------------------------------------
    # Pattern Methods
    # --------------------------------------------------

    def add_pattern(
        self,
        name: str,
        value: Any,
    ) -> None:

        self.patterns[name] = value

    def get_pattern(
        self,
        name: str,
        default: Any = None,
    ) -> Any:

        return self.patterns.get(
            name,
            default,
        )

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
    # Decision
    # --------------------------------------------------

    def approve(
        self,
        decision: str,
        reason: str = "",
    ) -> None:

        self.approved = True

        self.rejected = False

        self.decision = decision

        self.reason = reason

    def reject(
        self,
        decision: str,
        reason: str,
    ) -> None:

        self.approved = False

        self.rejected = True

        self.decision = decision

        self.reason = reason

    # --------------------------------------------------
    # Reset
    # --------------------------------------------------

    def reset(self) -> None:

        self.indicators.clear()

        self.patterns.clear()

        self.metadata.clear()

        self.approved = False

        self.rejected = False

        self.decision = ""

        self.reason = ""