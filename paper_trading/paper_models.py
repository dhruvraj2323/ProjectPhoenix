"""
=================================================
Project Phoenix
Paper Trading Models
M54
=================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any


# =================================================
# Order Type
# =================================================


class OrderType(Enum):
    """
    Supported order types.
    """

    MARKET = "MARKET"

    LIMIT = "LIMIT"

    STOP = "STOP"


# =================================================
# Order Status
# =================================================


class OrderStatus(Enum):
    """
    Order lifecycle status.
    """

    CREATED = "CREATED"

    PENDING = "PENDING"

    FILLED = "FILLED"

    CANCELLED = "CANCELLED"

    REJECTED = "REJECTED"


# =================================================
# Position Status
# =================================================


class PositionStatus(Enum):
    """
    Position lifecycle.
    """

    OPEN = "OPEN"

    CLOSED = "CLOSED"

    PARTIALLY_CLOSED = (
        "PARTIALLY_CLOSED"
    )


# =================================================
# Trade Status
# =================================================


class TradeStatus(Enum):
    """
    Trade execution status.
    """

    CREATED = "CREATED"

    RUNNING = "RUNNING"

    COMPLETED = "COMPLETED"

    FAILED = "FAILED"


# =================================================
# Execution Mode
# =================================================


class ExecutionMode(Enum):
    """
    Trading execution mode.
    """

    PAPER = "PAPER"

    DEMO = "DEMO"


# =================================================
# Paper Order
# =================================================


@dataclass(slots=True)
class PaperOrder:
    """
    Paper trading order.
    """

    order_id: str

    symbol: str

    order_type: OrderType

    direction: str

    volume: float

    entry_price: float

    stop_loss: float

    take_profit: float

    status: OrderStatus = (
        OrderStatus.CREATED
    )

    execution_mode: ExecutionMode = (
        ExecutionMode.PAPER
    )

    filled_price: float = 0.0

    commission: float = 0.0

    slippage: float = 0.0

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )

    metadata: dict[
        str,
        Any,
    ] = field(
        default_factory=dict,
    )

# =================================================
# Paper Position
# =================================================


@dataclass(slots=True)
class PaperPosition:
    """
    Active paper trading position.
    """

    position_id: str

    order_id: str

    symbol: str

    direction: str

    volume: float

    entry_price: float

    current_price: float = 0.0

    stop_loss: float = 0.0

    take_profit: float = 0.0

    floating_profit: float = 0.0

    realized_profit: float = 0.0

    status: PositionStatus = (
        PositionStatus.OPEN
    )

    opened_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )

    closed_at: datetime | None = None

    metadata: dict[
        str,
        Any,
    ] = field(
        default_factory=dict,
    )


# =================================================
# Paper Trade
# =================================================


@dataclass(slots=True)
class PaperTrade:
    """
    Completed paper trade.
    """

    trade_id: str

    position_id: str

    symbol: str

    direction: str

    volume: float

    entry_price: float

    exit_price: float

    profit_loss: float

    win: bool

    duration_seconds: float = 0.0

    status: TradeStatus = (
        TradeStatus.COMPLETED
    )

    opened_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )

    closed_at: datetime | None = None

    metadata: dict[
        str,
        Any,
    ] = field(
        default_factory=dict,
    )


# =================================================
# Paper Statistics
# =================================================


@dataclass(slots=True)
class PaperStatistics:
    """
    Paper trading statistics.
    """

    total_orders: int = 0

    total_positions: int = 0

    total_trades: int = 0

    winning_trades: int = 0

    losing_trades: int = 0

    win_rate: float = 0.0

    net_profit: float = 0.0

    gross_profit: float = 0.0

    gross_loss: float = 0.0

    average_profit: float = 0.0

    average_loss: float = 0.0


# =================================================
# Paper Result
# =================================================


@dataclass(slots=True)
class PaperResult:
    """
    Complete Paper Trading result.
    """

    approved: bool = False

    order: PaperOrder | None = None

    position: PaperPosition | None = None

    trade: PaperTrade | None = None

    statistics: PaperStatistics = field(
        default_factory=PaperStatistics,
    )

    reason: str = ""

    metadata: dict[
        str,
        Any,
    ] = field(
        default_factory=dict,
    )    