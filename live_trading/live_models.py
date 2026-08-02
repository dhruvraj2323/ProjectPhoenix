"""
=================================================
Project Phoenix
Live Trading Models
M55
=================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


# --------------------------------------------------
# Enumerations
# --------------------------------------------------


class OrderType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    BUY_LIMIT = "BUY_LIMIT"
    SELL_LIMIT = "SELL_LIMIT"
    BUY_STOP = "BUY_STOP"
    SELL_STOP = "SELL_STOP"


class PositionDirection(str, Enum):
    LONG = "LONG"
    SHORT = "SHORT"


class OrderStatus(str, Enum):
    PENDING = "PENDING"
    SUBMITTED = "SUBMITTED"
    FILLED = "FILLED"
    PARTIAL = "PARTIAL"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"


class BrokerType(str, Enum):
    MT5 = "MT5"
    PAPER = "PAPER"
    UNKNOWN = "UNKNOWN"


# --------------------------------------------------
# Live Order
# --------------------------------------------------


@dataclass(slots=True)
class LiveOrder:

    order_id: str = ""

    broker_order_id: str = ""

    symbol: str = ""

    order_type: OrderType = OrderType.BUY

    volume: float = 0.0

    price: float = 0.0

    stop_loss: float = 0.0

    take_profit: float = 0.0

    status: OrderStatus = OrderStatus.PENDING

    comment: str = ""

    created_at: datetime = field(
        default_factory=datetime.utcnow,
    )


# --------------------------------------------------
# Live Position
# --------------------------------------------------


@dataclass(slots=True)
class LivePosition:

    position_id: str = ""

    broker_position_id: str = ""

    symbol: str = ""

    direction: PositionDirection = PositionDirection.LONG

    volume: float = 0.0

    entry_price: float = 0.0

    current_price: float = 0.0

    stop_loss: float = 0.0

    take_profit: float = 0.0

    profit: float = 0.0

    swap: float = 0.0

    commission: float = 0.0

    opened_at: datetime = field(
        default_factory=datetime.utcnow,
    )

# --------------------------------------------------
# Live Trade
# --------------------------------------------------


@dataclass(slots=True)
class LiveTrade:

    trade_id: str = ""

    broker_ticket: str = ""

    symbol: str = ""

    direction: PositionDirection = PositionDirection.LONG

    entry_price: float = 0.0

    exit_price: float = 0.0

    volume: float = 0.0

    gross_profit: float = 0.0

    commission: float = 0.0

    swap: float = 0.0

    net_profit: float = 0.0

    opened_at: datetime = field(
        default_factory=datetime.utcnow,
    )

    closed_at: datetime = field(
        default_factory=datetime.utcnow,
    )

    duration: float = 0.0


# --------------------------------------------------
# Live Account
# --------------------------------------------------


@dataclass(slots=True)
class LiveAccount:

    account_id: str = ""

    broker: BrokerType = BrokerType.MT5

    server: str = ""

    balance: float = 0.0

    equity: float = 0.0

    margin: float = 0.0

    free_margin: float = 0.0

    margin_level: float = 0.0

    currency: str = "USD"

    leverage: float = 100.0

    updated_at: datetime = field(
        default_factory=datetime.utcnow,
    )


# --------------------------------------------------
# Execution Result
# --------------------------------------------------


@dataclass(slots=True)
class LiveExecutionResult:

    success: bool = False

    broker_ticket: str = ""

    retcode: int = 0

    message: str = ""

    filled_price: float = 0.0

    filled_volume: float = 0.0

    execution_time: datetime = field(
        default_factory=datetime.utcnow,
    )


# --------------------------------------------------
# Statistics
# --------------------------------------------------


@dataclass(slots=True)
class LiveStatistics:

    orders_sent: int = 0

    orders_filled: int = 0

    orders_rejected: int = 0

    positions_opened: int = 0

    positions_closed: int = 0

    winning_trades: int = 0

    losing_trades: int = 0

    gross_profit: float = 0.0

    gross_loss: float = 0.0

    net_profit: float = 0.0

    win_rate: float = 0.0


# --------------------------------------------------
# Engine Result
# --------------------------------------------------


@dataclass(slots=True)
class LiveResult:

    success: bool = False

    message: str = ""

    execution_result: LiveExecutionResult = field(
        default_factory=LiveExecutionResult,
    )

    statistics: LiveStatistics = field(
        default_factory=LiveStatistics,
    )

    completed_at: datetime = field(
        default_factory=datetime.utcnow,
    )    