"""
=================================================
Project Phoenix
Live Trading Context
M55
=================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from live_trading.live_models import (
    LiveAccount,
    LiveOrder,
    LivePosition,
    LiveResult,
    LiveStatistics,
    LiveTrade,
)


@dataclass(slots=True)
class LiveContext:
    """
    Shared runtime context for
    Live Trading Engine.
    """

    # --------------------------------------------------
    # Engine Information
    # --------------------------------------------------

    live_id: str

    account_id: str

    symbol: str

    timeframe: str

    created_at: datetime = field(
        default_factory=datetime.utcnow,
    )

    # --------------------------------------------------
    # Broker Information
    # --------------------------------------------------

    broker_name: str = ""

    server_name: str = ""

    # --------------------------------------------------
    # Runtime Input
    # --------------------------------------------------

    execution_result: Any = None

    market_price: float = 0.0

    spread: float = 0.0

    # --------------------------------------------------
    # Runtime Objects
    # --------------------------------------------------

    order: LiveOrder | None = None

    position: LivePosition | None = None

    trade: LiveTrade | None = None

    account: LiveAccount = field(
        default_factory=LiveAccount,
    )

    statistics: LiveStatistics = field(
        default_factory=LiveStatistics,
    )

    result: LiveResult = field(
        default_factory=LiveResult,
    )

    # --------------------------------------------------
    # Metadata
    # --------------------------------------------------

    metadata: dict[str, Any] = field(
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
        Mark Live Trading
        execution completed.
        """

        self.completed = True

        self.failed = False

    def fail(
        self,
        reason: str,
    ) -> None:
        """
        Mark Live Trading
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

        self.account = LiveAccount()

        self.statistics = (
            LiveStatistics()
        )

        self.result = (
            LiveResult()
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