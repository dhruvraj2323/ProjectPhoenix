"""
=================================================
Project Phoenix
Portfolio Context
M35
=================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from portfolio_engine.portfolio_models import (
    PortfolioPosition,
    PortfolioSummary,
)


@dataclass(slots=True)
class PortfolioContext:
    """
    Runtime context for Portfolio Engine.
    """

    portfolio_id: str

    account_id: str

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )

    positions: list[PortfolioPosition] = field(
        default_factory=list,
    )

    summary: PortfolioSummary = field(
        default_factory=PortfolioSummary,
    )

    metadata: dict = field(
        default_factory=dict,
    )

    approved: bool = False

    completed: bool = False

    failed: bool = False

    decision: str = ""

    reason: str = ""

    def approve(
        self,
        decision: str,
        reason: str,
    ) -> None:
        """
        Mark portfolio processing as approved.
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
        Mark portfolio processing as rejected.
        """

        self.approved = False

        self.completed = True

        self.failed = True

        self.decision = decision

        self.reason = reason

    def reset(self) -> None:
        """
        Reset execution state.
        """

        self.approved = False

        self.completed = False

        self.failed = False

        self.decision = ""

        self.reason = ""