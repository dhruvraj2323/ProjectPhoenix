"""
=================================================
Project Phoenix
Paper Trading Context
M24
=================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from paper_trading.paper_models import (
    PaperPortfolio,
    PaperPosition,
    PaperTradingResult,
)


@dataclass(slots=True)
class PaperContext:
    """
    Runtime context for Paper Trading Engine.
    """

    paper_id: str

    account_id: str

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )

    portfolio: PaperPortfolio = field(
        default_factory=PaperPortfolio,
    )

    positions: list[PaperPosition] = field(
        default_factory=list,
    )

    result: PaperTradingResult = field(
        default_factory=PaperTradingResult,
    )

    execution_result: object | None = None

    metadata: dict = field(
        default_factory=dict,
    )

    completed: bool = False

    failed: bool = False

    reason: str = ""

    def complete(self) -> None:
        """
        Mark processing as completed.
        """

        self.completed = True

        self.failed = False

    def fail(
        self,
        reason: str,
    ) -> None:
        """
        Mark processing as failed.
        """

        self.completed = False

        self.failed = True

        self.reason = reason