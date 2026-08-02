"""
=================================================
Project Phoenix
Paper Trading Context
M54
=================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from paper_trading.paper_models import (
    PaperOrder,
    PaperPosition,
    PaperTrade,
    PaperStatistics,
    PaperResult,
)


@dataclass(slots=True)
class PaperContext:
    """
    Shared runtime context for
    Paper Trading Engine.
    """

    # --------------------------------------------------
    # Engine Information
    # --------------------------------------------------

    paper_id: str

    account_id: str

    symbol: str

    timeframe: str

    created_at: datetime = field(
        default_factory=datetime.utcnow,
    )

    # --------------------------------------------------
    # Input
    # --------------------------------------------------

    execution_result: Any = None

    market_price: float = 0.0

    spread: float = 0.0

    balance: float = 100000.0

    equity: float = 100000.0

    leverage: float = 100.0

    # --------------------------------------------------
    # Runtime Objects
    # --------------------------------------------------

    order: PaperOrder | None = None

    position: PaperPosition | None = None

    trade: PaperTrade | None = None

    statistics: PaperStatistics = field(
        default_factory=PaperStatistics,
    )

    result: PaperResult = field(
        default_factory=PaperResult,
    )

    # --------------------------------------------------
    # Metadata
    # --------------------------------------------------

    metadata: dict[
        str,
        Any,
    ] = field(
        default_factory=dict,
    )

    # --------------------------------------------------
    # Runtime State
    # --------------------------------------------------

    completed: bool = False

    failed: bool = False

    reason: str = ""

    # --------------------------------------------------
    # Utility Methods
    # --------------------------------------------------

    def complete(
        self,
    ) -> None:
        """
        Mark Paper Trading
        execution completed.
        """

        self.completed = True

        self.failed = False

    def fail(
        self,
        reason: str,
    ) -> None:
        """
        Mark Paper Trading
        execution failed.
        """

        self.completed = False

        self.failed = True

        self.reason = reason

    def reset(
        self,
    ) -> None:
        """
        Reset runtime state.
        """

        self.order = None

        self.position = None

        self.trade = None

        self.statistics = (
            PaperStatistics()
        )

        self.result = (
            PaperResult()
        )

        self.metadata.clear()

        self.market_price = 0.0

        self.spread = 0.0

        self.completed = False

        self.failed = False

        self.reason = ""

    def set_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Store metadata.
        """

        self.metadata[key] = value