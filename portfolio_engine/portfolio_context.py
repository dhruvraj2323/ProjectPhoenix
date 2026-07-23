"""
=================================================
Project Phoenix
Portfolio Context
M35
=================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from portfolio_engine.portfolio_models import (
    PortfolioStatistics,
    Position,
)


@dataclass(slots=True)
class PortfolioContext:
    """
    Shared runtime context for Portfolio Engine.
    """

    engine_id: str
    account_id: str

    balance: float = 0.0
    equity: float = 0.0
    margin: float = 0.0
    free_margin: float = 0.0

    created_at: datetime = field(
        default_factory=datetime.utcnow
    )

    positions: list[Position] = field(
        default_factory=list
    )

    statistics: PortfolioStatistics = field(
        default_factory=PortfolioStatistics
    )

    metadata: dict = field(
        default_factory=dict
    )

    completed: bool = False
    failed: bool = False
    reason: str = ""

    def add_position(
        self,
        position: Position,
    ) -> None:
        self.positions.append(position)

    def remove_position(
        self,
        symbol: str,
    ) -> None:

        self.positions = [
            p
            for p in self.positions
            if p.symbol != symbol
        ]

    def reset(self) -> None:

        self.positions.clear()

        self.statistics = PortfolioStatistics()

        self.metadata.clear()

        self.completed = False

        self.failed = False

        self.reason = ""