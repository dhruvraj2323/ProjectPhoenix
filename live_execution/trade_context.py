"""
=================================================
Project Phoenix
Live Trade Context
M59.1.2
=================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from live_execution.trade_models import (
    TradeRequest,
    TradeResponse,
)


@dataclass(
    slots=True,
)
class TradeContext:
    """
    Runtime context for the
    Live Trade Execution Engine.
    """

    # --------------------------------------------------
    # Execution Information
    # --------------------------------------------------

    execution_id: str

    symbol: str

    timeframe: str

    # --------------------------------------------------
    # Upstream Engine Results
    # --------------------------------------------------

    strategy_result: Any = None

    signal_result: Any = None

    risk_result: Any = None

    ai_result: Any = None

    # --------------------------------------------------
    # Trade Objects
    # --------------------------------------------------

    trade_request: (
        TradeRequest | None
    ) = None

    trade_response: (
        TradeResponse | None
    ) = None

    # --------------------------------------------------
    # Runtime Metadata
    # --------------------------------------------------

    metadata: dict[
        str,
        object,
    ] = field(
        default_factory=dict,
    )

    # --------------------------------------------------
    # Status
    # --------------------------------------------------

    completed: bool = False

    failed: bool = False

    reason: str = ""

    # --------------------------------------------------
    # Utility
    # --------------------------------------------------

    def complete(
        self,
    ) -> None:

        self.completed = True

        self.failed = False

    def fail(
        self,
        reason: str,
    ) -> None:

        self.completed = False

        self.failed = True

        self.reason = reason

    def set_metadata(
        self,
        key: str,
        value: object,
    ) -> None:

        self.metadata[
            key
        ] = value

    def get_metadata(
        self,
        key: str,
        default: object = None,
    ) -> object:

        return self.metadata.get(
            key,
            default,
        )