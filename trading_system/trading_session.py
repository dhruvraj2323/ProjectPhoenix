"""
=================================================
Project Phoenix
Trading Session
M39
=================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(slots=True)
class TradingSession:
    """
    Represents one complete trading session.
    """

    # --------------------------------------------------
    # Session Information
    # --------------------------------------------------

    session_id: str

    started_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    ended_at: datetime | None = None

    # --------------------------------------------------
    # Session Status
    # --------------------------------------------------

    active: bool = True

    completed: bool = False

    # --------------------------------------------------
    # Statistics
    # --------------------------------------------------

    total_trades: int = 0

    successful_trades: int = 0

    failed_trades: int = 0

    skipped_trades: int = 0

    # --------------------------------------------------
    # Performance
    # --------------------------------------------------

    gross_profit: float = 0.0

    gross_loss: float = 0.0

    net_profit: float = 0.0

    # --------------------------------------------------
    # Utility Methods
    # --------------------------------------------------

    def record_success(
        self,
        profit: float = 0.0,
    ) -> None:
        """
        Record successful trade.
        """

        self.total_trades += 1

        self.successful_trades += 1

        self.gross_profit += profit

        self.net_profit += profit

    def record_failure(
        self,
        loss: float = 0.0,
    ) -> None:
        """
        Record failed trade.
        """

        self.total_trades += 1

        self.failed_trades += 1

        self.gross_loss += loss

        self.net_profit -= loss

    def record_skip(self) -> None:
        """
        Record skipped trade.
        """

        self.skipped_trades += 1

    def close(self) -> None:
        """
        Close trading session.
        """

        self.active = False

        self.completed = True

        self.ended_at = datetime.now(UTC)

    def reset(self) -> None:
        """
        Reset session statistics.
        """

        self.total_trades = 0

        self.successful_trades = 0

        self.failed_trades = 0

        self.skipped_trades = 0

        self.gross_profit = 0.0

        self.gross_loss = 0.0

        self.net_profit = 0.0

        self.active = True

        self.completed = False

        self.started_at = datetime.now(UTC)

        self.ended_at = None