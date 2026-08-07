"""
=================================================
Project Phoenix
Live Trade Models
M59.1.1
=================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


# ==================================================
# Order Side
# ==================================================


class OrderSide(
    Enum,
):
    """
    Trade direction.
    """

    BUY = "BUY"

    SELL = "SELL"


# ==================================================
# Execution Status
# ==================================================


class ExecutionStatus(
    Enum,
):
    """
    Trade execution result.
    """

    PENDING = "PENDING"

    EXECUTED = "EXECUTED"

    REJECTED = "REJECTED"

    FAILED = "FAILED"


# ==================================================
# Execution Type
# ==================================================


class ExecutionType(
    Enum,
):
    """
    Order execution type.
    """

    MARKET = "MARKET"

    LIMIT = "LIMIT"

    STOP = "STOP"


# ==================================================
# Trade Request
# ==================================================


@dataclass(
    slots=True,
)
class TradeRequest:
    """
    Phoenix trade request.
    """

    symbol: str

    volume: float

    side: OrderSide

    execution_type: ExecutionType

    price: float

    stop_loss: float

    take_profit: float

    deviation: int = 20

    magic_number: int = 590001

    comment: str = "Project Phoenix"


# ==================================================
# Trade Response
# ==================================================


@dataclass(
    slots=True,
)
class TradeResponse:
    """
    Phoenix execution result.
    """

    status: ExecutionStatus

    ticket: int | None = None

    executed_price: float = 0.0

    executed_volume: float = 0.0

    broker_message: str = ""

    execution_time: datetime | None = None

    retcode: int = 0